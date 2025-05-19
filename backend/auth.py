from datetime import datetime, timedelta
from jose import JWTError, jwt
from dotenv import load_dotenv
import os

load_dotenv()

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        return payload  # Bevat o.a. 'sub' (email)
    except JWTError:
        return None
