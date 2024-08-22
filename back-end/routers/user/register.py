from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from utils.mysql import get_db, execute_query

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class RegisterResponse(BaseModel):
    success: bool
    message: str


def get_password_hash(password):
    return pwd_context.hash(password)


def create_user(connection, user: UserCreate):
    query = "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)"
    hashed_password = get_password_hash(user.password)
    values = (user.username, user.email, hashed_password)
    execute_query(connection, query, values)


@router.post("/register")
async def register(user: UserCreate, db=Depends(get_db)):
    try:
        check_username_query = "SELECT * FROM users WHERE username = %s"
        existing_username = execute_query(
            db, check_username_query, (user.username,), fetch_method="fetchone"
        )
        if existing_username:
            return JSONResponse(
                status_code=400, content={"data": {"error": "Username already taken"}}
            )

        check_email_query = "SELECT * FROM users WHERE email = %s"
        existing_email = execute_query(
            db, check_email_query, (user.email,), fetch_method="fetchone"
        )
        if existing_email:
            return JSONResponse(
                status_code=400, content={"data": {"error": "Email already registered"}}
            )

        create_user(db, user)
        return JSONResponse(
            status_code=200,
            content={"data": {"message": "User registered successfully"}},
        )
    except Exception as e:
        return JSONResponse(status_code=500, content={"data": {"error": str(e)}})
