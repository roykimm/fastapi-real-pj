from app.database import MyDatabase
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, Depends, status
from app.services.user import get_user_by_username

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# openssl rand -hex 32
SECRET_KEY = 'c844e68f13e58a0f66aae2d1973c489dc1f7dff7374bb3c23e69b40783a56af1'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def get_user(username: str):
    with MyDatabase() as db:
        db.cursor.execute(f"""
            select id, username, password
              from users
             where username = '{username}'
        """)

        result = db.cursor.fetchone()
        obj = {
            "id": result[0],
            "username": result[1],
            "password": result[2],
        }
        print(obj)
    return obj


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user_by_username(username=username)
    if user is None:
        raise credentials_exception
    return user
