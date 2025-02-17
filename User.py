from typing import Annotated
import secrets
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi.security import HTTPBasic, HTTPBasicCredentials


class UserBase(SQLModel):
    name: str = Field(index=True)
    description: str = Field(index=True)
    avatar: str = Field(index=False)
    role: str | None = Field(default=False)


class User(UserBase):
    id: int | None = Field(default=None, primary_key=True)
    password: str


class UserPublic(UserBase):
    name: str
    description: str
    avatar: str = Field(index=False)
    role: str
    id: int


class UserCreate(UserBase):
    name: str
    password: str


class UserUpdate(UserBase):
    name: str | None = None
    description: str | None = None
    avatar: str | None = None


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/user/", response_model=UserPublic)
def create_User(User: UserCreate, session: SessionDep):
    db_User = User.model_validate(User)
    session.add(db_User)
    session.commit()
    session.refresh(db_User)
    return db_User


@app.get("/user/", response_model=list[UserPublic])
def read_User(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    User = session.exec(select(User).offset(offset).limit(limit)).all()
    return User


@app.patch("/user/{User_id}", response_model=UserPublic)
def update_User(user_id: int, user: UserUpdate, session: SessionDep):
    User_db = session.get(User, user_id)
    if not User_db:
        raise HTTPException(status_code=404, detail="User not found")
    User_data = User.model_dump(exclude_unset=True)
    User_db.sqlmodel_update(User_data)
    session.add(User_db)
    session.commit()
    session.refresh(User_db)
    return User_db


@app.delete("/user/{User_id}")
def delete_User(User_id: int, session: SessionDep):
    User = session.get(User, User_id)
    if not User:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(User)
    session.commit()
    return {"ok": True}


app = FastAPI()


security = HTTPBasic()


def get_current_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = b"stanleyjobson"
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = b"swordfish"
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/users/me")
def read_current_user(username: Annotated[str, Depends(get_current_username)]):
    return {"username": username}