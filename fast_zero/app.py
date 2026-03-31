from http import HTTPStatus

from fastapi import FastAPI

from fast_zero.routers import auth, todos, users, pdf
from fast_zero.schemas import Message

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(pdf.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}


@app.get('/pdf/test')
async def test_pdf_endpoint():
    return {
        'status': 'ok',
        'message': 'PDF endpoint está funcionando',
        'pdf_extractor_loaded': True
    }