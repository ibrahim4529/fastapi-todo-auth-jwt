from fastapi import APIRouter, HTTPException, Depends
from app.models import User
from sqlmodel import Session, select
from app.schemas import UserLogin, UserToken, UserRegister, UserRead
from app.db import get_session
from app.utils import ( hash_password, verify_password, 
    create_jwt_token, get_active_user)

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

def authenticate_user(session: Session,  username: str, password: str):
    statement = select(User).where(User.username == username)
    results = session.exec(statement)
    user = results.first()
    if user is None:
        return False
    if not verify_password(password=password, hashed=user.password):
        return False
    return user


@router.post("/login", response_model=UserToken)
def login(user_data: UserLogin, db: Session = Depends(get_session)):
    user = authenticate_user(db, user_data.username, user_data.password)
    print(user)
    if not user:
        raise HTTPException(401, detail="Incorrect username or password")
    token = create_jwt_token({"sub": str(user.id)})
    print(user.id)
    return {
        "user": user,
        "token": token
    }


@router.post("/register", response_model=UserRead)
def register(user_data: UserRegister, db: Session = Depends(get_session)):
    user = authenticate_user(db, user_data.username, user_data.password)
    if user:
        raise HTTPException(status_code=400, detail="User already exists")
    user = User(
        username=user_data.username,
        password=hash_password(user_data.password),
        email=user_data.email
    )
    db.add(user)
    db.commit()
    return user

@router.get("/me", response_model=UserRead)
def me(user: User = Depends(get_active_user)):
    return user
