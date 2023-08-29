from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine
from fastapi.security import HTTPBearer
from jwt import create_token

models.Base.metadata.create_all(bind=engine)

user_create_router = APIRouter()

oauth2_scheme = HTTPBearer(
    scheme_name="JWTBearer",
    bearerFormat='jwt'
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@user_create_router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_login(db, login=user.login)
    tok = create_token(data={"sub": f"{user.login}"})
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    crud.create_user(db=db, user=user)
    return schemas.User(login=user.login, token=tok)


@user_create_router.get("/user/")
def get_user_by_token(jwt: dict = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = crud.get_user_by_jwt(db=db, jwt=jwt)
    if user is None or jwt is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
