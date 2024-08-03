from fastapi.testeclient import TesteClient

from fast_zero.app import app

client = TesteClient(app)
