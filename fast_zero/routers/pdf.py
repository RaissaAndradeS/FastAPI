# fast_zero/pdf.py
import os
import logging
from tempfile import NamedTemporaryFile

from fastapi import APIRouter, File, HTTPException, UploadFile, status
from fastapi.responses import HTMLResponse, JSONResponse

from fast_zero.pdf_extractor import extract_pdf_data

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter(prefix='/pdf', tags=['pdf'])


@router.post('/extract')
async def extract_pdf(file: UploadFile = File(...)):
    logger.info(f"Recebendo arquivo: {file.filename}")
    logger.info(f"Content-Type: {file.content_type}")
    
    if file.content_type not in ('application/pdf', 'application/octet-stream'):
        logger.error(f"Content-Type inválido: {file.content_type}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Envie um arquivo PDF',
        )

    contents = await file.read()
    logger.info(f"Tamanho do arquivo: {len(contents)} bytes")
    
    # Salvar o arquivo temporário e processar
    tmp_path = None
    try:
        with NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
            tmp.write(contents)
            tmp_path = tmp.name
            logger.info(f"Arquivo temporário criado: {tmp_path}")
            logger.info(f"Tamanho do arquivo no disco: {os.path.getsize(tmp_path)} bytes")
        
        # Verificar se o arquivo é um PDF válido
        import magic
        try:
            mime = magic.from_file(tmp_path, mime=True)
            logger.info(f"MIME type detectado: {mime}")
        except:
            logger.warning("python-magic não instalado, pulando verificação MIME")
        
        result = extract_pdf_data(tmp_path)
        logger.info(f"Resultado da extração: {result}")
        logger.info(f"Tabelas encontradas: {result.get('table_count', 0)}")
        
        # Log detalhado das tabelas
        for i, table in enumerate(result.get('tables', [])):
            logger.info(f"Tabela {i}: página={table.get('page')}, source={table.get('source')}, colunas={len(table.get('columns', []))}, linhas={len(table.get('rows', []))}")
        
    except Exception as e:
        logger.error(f"Erro durante processamento: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={'error': str(e), 'file_name': file.filename}
        )
    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
                logger.info(f"Arquivo temporário removido: {tmp_path}")
            except OSError as e:
                logger.error(f"Erro ao remover arquivo temporário: {e}")

    return result