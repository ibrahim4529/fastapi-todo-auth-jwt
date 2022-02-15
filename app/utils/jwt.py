from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import select, Session
from app.models import User
from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.config import get_config
from app.db import get_session


config = get_config()

class JWTAuthentication(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTAuthentication, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTAuthentication, self).__call__(request)
        if credentials:
            return self.get_user_id(credentials.credentials)
        else:
            raise HTTPException(status_code=403, detail="Tidak Ada credentials.")

    def get_user_id(self, token: str) -> str:
        print(token)
        try:
            payload = jwt.decode(token, config.SECRET_KEY, algorithms=config.JWT_ALGORITHM)
            return payload['sub']
        except JWTError as err:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")


jwt_security = JWTAuthentication()


def create_jwt_token(payload: dict) -> str:
    expire = datetime.utcnow() + timedelta(hours=config.JWT_EXPIRE_TIME_HOUR)
    to_encode = payload.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.JWT_ALGORITHM)


async def get_active_user(session: Session = Depends(get_session), user_id: str = Depends(jwt_security)):
    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=403, detail="Invalid authorization code.")
    return user