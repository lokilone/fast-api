from fastapi import FastAPI
from fastapi import Header
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

# users_db

users_db ={
    "alice": "wonderland",
    "bob": "builder",
    "clementine": "mandarine"
    }

@app.get('/users')
def get_users():
    return users_db
# curl -X GET -i http://127.0.0.1:8000/users

@app.get('/users/{username}')
def get_user(username):
    password = users_db.get(username)
    return {username: password}
# curl -X GET -i http://127.0.0.1:8000/users/alice

# Créer utilisateur
@app.put('/users')
def put_users(username, password):
    users_db[username]=password
    return {username: password}

# Modifier utilisateur
@app.post('/users/{username}')
def post_user(username, password):
    try:
        users_db[username]=password
        return {username: password}
    except IndexError:
        return {}


# supprimer utilisateur
@app.delete('/users/{username}')
def delete_user(username):
    try:
        del users_db[username]
        return {
            'deleted': True
            }
    except IndexError:
        return {}

