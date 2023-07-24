from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext

app = FastAPI()
security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

users = {

    "daniel": {
        "username": "daniel",
        "name": "Daniel Datascientest",
        "hashed_password": pwd_context.hash('datascientest'),
    },

    "john" : {
        "username" :  "john",
        "name" : "John Datascientest",
        "hashed_password" : pwd_context.hash('secret'),
    }

}

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    if not(users.get(username)) or not(pwd_context.verify(credentials.password, users[username]['hashed_password'])):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get("/user")
def current_user(username: str = Depends(get_current_user)):
    return "Hello {}".format(username)