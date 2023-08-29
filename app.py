from fastapi import FastAPI
from api.user import user_create_router

app = FastAPI()

app.include_router(user_create_router)


@app.get('/')
async def info():
    return {
        'status': 'ok',
        'msg': "Hello to my API"
    }
