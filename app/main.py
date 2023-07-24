from fastapi import FastAPI
from fastapi import Header
from pydantic import BaseModel
from typing import Optional, List

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext

app = FastAPI()
security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

users ={
    "alice": "wonderland",
    "bob": "builder",
    "clementine": "mandarine"
    }

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    if not(users.get(username)) or not(pwd_context.verify(credentials.password, users[username])):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get("/user")
def current_user(username: str = Depends(get_current_user)):
    return "Hello {}".format(username)

@app.get('/users')
def get_users():
    return users.keys
# curl -X GET -i http://127.0.0.1:8000/users

@app.get('/users/{username}')
def get_user(username):
    password = users.get(username)
    return {username: password}
# curl -X GET -i http://127.0.0.1:8000/users/alice