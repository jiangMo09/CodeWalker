from fastapi import APIRouter, Depends, Request, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional
import jwt
from passlib.context import CryptContext
from utils.mysql import get_db, execute_query
from utils.load_env import JWT_SECRET_KEY

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Token(BaseModel):
    access_token: str
    token_type: str


class LoginResponse(BaseModel):
    success: bool
    message: str
    token: Optional[Token] = None


class LoginRequest(BaseModel):
    email: str
    password: str


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(connection, email, password):
    query = "SELECT * FROM users WHERE email = %s"
    user = execute_query(connection, query, (email,), fetch_method="fetchone")
    if user and verify_password(password, user["password_hash"]):
        return user
    return None


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    jwt_token = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm="HS256")
    return jwt_token


@router.post("/login")
async def login(form_data: LoginRequest, db=Depends(get_db)):
    try:
        user = authenticate_user(db, form_data.email, form_data.password)
        if not user:
            return JSONResponse(
                status_code=400,
                content={"data": {"error": "Incorrect username or password"}},
            )
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={
                "id": user["id"],
                "username": user["username"],
            },
            expires_delta=access_token_expires,
        )
        return JSONResponse(
            status_code=200,
            content={
                "data": {
                    "success": True,
                    "message": "Login successful",
                    "id": user["id"],
                    "username": user["username"],
                    "token": {"access_token": access_token, "token_type": "bearer"},
                }
            },
        )
    except Exception as e:
        return JSONResponse(status_code=500, content={"data": {"error": str(e)}})


@router.get("/verify_token")
async def verify_token(request: Request):
    auth_token = request.headers.get("authToken")
    if not auth_token:
        return {"data": None}

    try:
        payload = jwt.decode(auth_token, JWT_SECRET_KEY, algorithms=["HS256"])
        print("Decoded payload:", payload)
        return {"data": payload}
    except jwt.ExpiredSignatureError:
        print("Token expired")
        return {"data": None}
    except jwt.InvalidTokenError as err:
        print("Invalid token:", str(err))
        return {"data": None}
    except Exception as e:
        print("Unexpected error:", str(e))
        return {"data": None}
