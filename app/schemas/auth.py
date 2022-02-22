from sqlmodel import SQLModel

class UserAuthBase(SQLModel):
    username: str


class UserLogin(UserAuthBase):
    password: str


class UserRead(UserAuthBase):
    id: int
    email: str


class UserRegister(UserLogin):
    email: str

class UserToken(SQLModel):
    token: str
    user: UserRead