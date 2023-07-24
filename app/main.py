from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()
security = HTTPBasic()

users ={
    "alice": "wonderland",
    "bob": "builder",
    "clementine": "mandarine"
    }

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    if not(users.get(username)) or credentials.password != users.get(username):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get("/user")
def current_user(username: str = Depends(get_current_user)):
    return f"Hello {username}"

@app.get('/users')
def get_users():
    return list(users.keys())
# curl -X GET -i http://127.0.0.1:8000/users

# @app.get('/users/{username}')
# def get_user(username):
#     password = users.get(username)
#     return {username: password}
# # curl -X GET -i http://127.0.0.1:8000/users/alice