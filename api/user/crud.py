from sqlalchemy.orm import Session
from jwt import decode_token

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_login(db: Session, login: str):
    return db.query(models.User).filter(models.User.login == login).first()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(login=user.login, passw=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_jwt(db: Session, jwt: dict):
    token = str(dict(jwt).get('credentials'))
    login = str(decode_token(token)['sub'])
    user = db.query(models.User).filter(models.User.login == login).first()
    return schemas.User(
        login=user.login,
        token=token
    )
