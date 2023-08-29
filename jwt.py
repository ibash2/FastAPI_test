from jose import jwt
from datetime import datetime, timedelta
from config import AppConfig


def create_token(data: dict, expiredelta: timedelta = None):
    to_en = data.copy()
    if expiredelta:
        expire = datetime.utcnow() + expiredelta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_en.update({'exp': expire})
    encoded_jwt = jwt.encode(to_en, AppConfig.SECRET_KEY)
    return encoded_jwt


def decode_token(token):
    try:
        payload = jwt.decode(token, AppConfig.SECRET_KEY)
        return payload
    except():
        return None
