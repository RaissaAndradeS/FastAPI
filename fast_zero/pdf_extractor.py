import re
from pathlib import Path
from typing import Any

import pdfplumber
import pandas as pd


def extract_pdf_data(file_path: str) -> dict[str, Any]:
    """
    Extrai dados do PDF e processa no formato necessário para o SEI.
    
    Args:
        file_path: Caminho para o arquivo PDF
        
    Returns:
        Dicionário com os dados extraídos e processados
    """
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f'Nenhum arquivo encontrado em {file_path}')
    
    
    all_tables = []
    
    try:
        with pdfplumber.open(str(path)) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                # Extrair tabelas da página
                extracted_tables = page.extract_tables()
                
                for table_data in extracted_tables:
                    if table_data and len(table_data) > 1:  
                        df = pd.DataFrame(table_data)
                        all_tables.append({
                            'page': page_num,
                            'df': df
                        })
    except Exception as e:
        return {
            'file_name': path.name,
            'table_count': 0,
            'tables': [],
            'error': f'Erro ao ler PDF: {str(e)}'
        }
    
    if not all_tables:
        return {
            'file_name': path.name,
            'table_count': 0,
            'tables': [],
            'error': 'Nenhuma tabela encontrada no PDF'
        }
    
    
    processed_tables = []
    for table_idx, table_info in enumerate(all_tables):
        try:
            df = table_info['df'].copy()
            
            # Processar a tabela
            processed_df = process_table(df)
            
            if not processed_df.empty:
                
                processed_tables.append({
                    'source': 'pdfplumber',
                    'page': str(table_info['page']),
                    'table_index': table_idx,
                    'columns': processed_df.columns.tolist(),
                    'rows': processed_df.to_dict('records'),
                    'html': processed_df.to_html(index=False, border=0, classes='table table-bordered')
                })
        except Exception as e:
            print(f"Erro ao processar tabela {table_idx}: {e}")
            continue
    
    return {
        'file_name': path.name,
        'table_count': len(processed_tables),
        'tables': processed_tables
    }


def process_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Processa uma tabela extraída do PDF no formato necessário.
    
    Args:
        df: DataFrame com os dados brutos da tabela
        
    Returns:
        DataFrame processado com as colunas no formato correto
    """
    if df.empty:
        return pd.DataFrame()
    
    df = df.fillna('')
    df = df.astype(str)
    
    # Remover linhas completamente vazias
    df = df[df.apply(lambda row: any(cell.strip() for cell in row), axis=1)]
    
    if df.empty:
        return pd.DataFrame()
    
    df_final = df.copy()
    
    def identificar_tipo_linha(row):
        has_proposal = len(row) > 3 and row.iloc[3] and row.iloc[3].strip()
        has_proposal_rev = len(row) > 4 and row.iloc[4] and row.iloc[4].strip()
        has_results = len(row) > 6 and row.iloc[6] and row.iloc[6].strip()
        
        if has_proposal or has_proposal_rev or has_results:
            return 'teste'
        else:
            return 'tabela'
    
    df_final['tipo_tabela'] = df_final.apply(identificar_tipo_linha, axis=1)
    
    # Processar as colunas conforme o tipo
    def processar_linha(row):
        if row['tipo_tabela'] == 'tabela':
            return pd.Series({
                'requirement': row.iloc[0] if len(row) > 0 else '',
                'moc': row.iloc[1] if len(row) > 1 else '',
                'title': row.iloc[2] if len(row) > 2 else '',
                'doc_id': row.iloc[5] if len(row) > 5 else '',
                'rev': row.iloc[7] if len(row) > 7 else '',
                'specialist': row.iloc[8] if len(row) > 8 else '',
                'proposal_id': '',
                'proposal_rev': '',
                'results_id': '',
                'results_rev': '',
                'doc_type': ''
            })
        else:  # tipo 'teste'
            return pd.Series({
                'requirement': row.iloc[0] if len(row) > 0 else '',
                'moc': row.iloc[1] if len(row) > 1 else '',
                'title': row.iloc[2] if len(row) > 2 else '',
                'doc_id': '',
                'rev': '',
                'specialist': row.iloc[8] if len(row) > 8 else '',
                'proposal_id': row.iloc[3] if len(row) > 3 else '',
                'proposal_rev': row.iloc[4] if len(row) > 4 else '',
                'results_id': row.iloc[6] if len(row) > 6 else '',
                'results_rev': row.iloc[7] if len(row) > 7 else '',
                'doc_type': ''
            })
    
    # Aplicar processamento
    df_processado = df_final.apply(processar_linha, axis=1)
    df_final = pd.concat([df_final, df_processado], axis=1)
    
    # Limpeza de cabeçalhos e linhas vazias
    mask = ~df_final[0].astype(str).str.contains(
        "Airworthiness Requirements|MoC|Requirement|MOC", 
        na=False, 
        case=False
    )
    df_final = df_final[mask]
    
    # Remover linhas onde a primeira coluna está vazia
    df_final = df_final[df_final[0].astype(str).str.strip() != '']
    df_final = df_final.reset_index(drop=True)
    
    if df_final.empty:
        return pd.DataFrame()
    
    cols_to_keep = ['requirement', 'moc', 'title', 'doc_id', 'rev', 
                    'proposal_id', 'proposal_rev', 'results_id', 'results_rev', 
                    'specialist', 'tipo_tabela']
    existing_cols = [col for col in cols_to_keep if col in df_final.columns]
    df_final = df_final[existing_cols]
    
    def expandir_titulos(row):
        rows_expandidas = []
        
        if row.get('tipo_tabela') == 'teste':
            title_text = str(row.get('title', ''))
            
            # Verificar se o título contém "PROPOSAL" e "RESULT"
            if "PROPOSAL" in title_text.upper() and "RESULT" in title_text.upper():
                # Dividir em partes
                partes = re.split(r'\s{2,}|\n', title_text)
                partes = [p.strip() for p in partes if p.strip()]
                
                for parte in partes:
                    new_row = row.copy()
                    new_row['title'] = parte
                    
                    # Identificar o tipo de documento
                    if "PROPOSAL" in parte.upper():
                        new_row['doc_type'] = 'proposal'
                        new_row['results_id'] = ''
                        new_row['results_rev'] = ''
                    elif "RESULT" in parte.upper():
                        new_row['doc_type'] = 'result'
                        new_row['proposal_id'] = ''
                        new_row['proposal_rev'] = ''
                    else:
                        new_row['doc_type'] = 'other'
                    
                    rows_expandidas.append(new_row)
            else:
                rows_expandidas.append(row)
        else:
            rows_expandidas.append(row)
        
        return rows_expandidas
    
    # Expandir títulos
    expanded_rows = []
    for _, row in df_final.iterrows():
        expanded_rows.extend(expandir_titulos(row))
    
    if not expanded_rows:
        return pd.DataFrame()
    
    df_final = pd.DataFrame(expanded_rows).reset_index(drop=True)
    
    # Remover a coluna temporária
    if 'tipo_tabela' in df_final.columns:
        df_final = df_final.drop(columns=['tipo_tabela'])
    
    # Limpeza adicional dos títulos
    df_final['title'] = df_final['title'].astype(str).str.strip()
    df_final['title'] = df_final['title'].str.replace(r'\s+', ' ', regex=True)
    
    # Renomear as colunas para o formato final
    rename_map = {
        "requirement": "Airworthiness Requirements",
        "moc": "MoC",
        "title": "Title",
        "doc_id": "Doc Id",
        "rev": "Rev Doc",
        "proposal_id": "Proposal Id",
        "proposal_rev": "Rev Proposal",
        "results_id": "Results Id",
        "results_rev": "Rev Results",
        "specialist": "Specialists Qualification",
        "doc_type": "Document Type"
    }
    
    
    for old_name, new_name in rename_map.items():
        if old_name in df_final.columns:
            df_final = df_final.rename(columns={old_name: new_name})
    
    
    if "Airworthiness Requirements" in df_final.columns:
        df_final["Airworthiness Requirements"] = (
            df_final["Airworthiness Requirements"]
            .astype(str)
            .str.replace("\n", "; ")
        )
    
    
    df_final = df_final.fillna('')
    
    
    if not df_final.empty and "Title" in df_final.columns:
        
        df_final["id_linha"] = df_final.index
        
        
        if "Airworthiness Requirements" in df_final.columns:
            df_final["Airworthiness Requirements"] = df_final["Airworthiness Requirements"].astype(str)
        
        
        df_final["atividades"] = df_final["Title"].astype(str).str.split("\n")
        
        
        df_exp = df_final.explode("atividades")
        
        
        df_exp["atividades"] = df_exp["atividades"].str.strip()
        
        
        df_exp = df_exp[df_exp["atividades"] != '']
        
        if not df_exp.empty:
            
            if "Airworthiness Requirements" in df_exp.columns:
                df_exp["Airworthiness Requirements"] = df_exp.groupby("id_linha")["Airworthiness Requirements"] \
                    .transform(lambda x: [x.iloc[0]] + [""] * (len(x) - 1))
            
            
            df_exp["Title"] = df_exp["atividades"]
            
            
            df_exp = df_exp.drop(columns=["id_linha", "atividades"])
            
            # Reordenar colunas
            column_order = [
                "Airworthiness Requirements", "MoC", "Title", "Doc Id", "Rev Doc",
                "Proposal Id", "Rev Proposal", "Results Id", "Rev Results",
                "Specialists Qualification", "Document Type"
            ]
            
            # Selecionar apenas as colunas que existem
            existing_columns = [col for col in column_order if col in df_exp.columns]
            df_exp = df_exp[existing_columns]
            
            return df_exp
    
    return df_final