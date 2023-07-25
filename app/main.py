# Start the FastAPI application using the command uvicorn main:app --reload.

# Import necessary libraries: pandas for data manipulation, FastAPI for building the web application, and other required dependencies.
import pandas as pd
from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Optional, List
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import json

# Create an instance of the FastAPI application.
app = FastAPI()
security = HTTPBasic()

# Define a dictionary called users that contains predefined username-password pairs for authentication.
users ={
    "alice": "wonderland",
    "bob": "builder",
    "clementine": "mandarine",
    "admin": "4dm1N"
    }

# Create a function get_current_user that authenticates users based on Basic HTTP Authentication.
def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    if not(users.get(username)) or credentials.password != users.get(username):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# Create a route /user that returns a greeting message to the authenticated user.
@app.get("/user")
def current_user(username: str = Depends(get_current_user)):
    return f"Hello {username}"

# @app.get('/users')
# def get_users(username: str = Depends(get_current_user)):
#     return {'Users list' : list(users.keys())}
# # curl -X GET -i http://127.0.0.1:8000/users

# @app.get('/users/{username}')
# def get_user(username: str = Depends(get_current_user)):
#     password = users.get(username)
#     return {username: password}
# # curl -X GET -i http://127.0.0.1:8000/users/alice

# # Load the data from the CSV file questions.csv into a DataFrame called df. Extract unique values from the 'use' and 'subject' columns into separate lists.
df = pd.read_csv('questions.csv')
# df = df[df.columns[df.columns != "correct"]]
use_lst = list(df['use'].unique())
subject_lst = list(df['subject'].unique())

# # Define a route /select that returns two lists: "Use list" and "Subject list" obtained from the loaded CSV file (questions.csv).
@app.get('/select')
def get_index(username: str = Depends(get_current_user)):
    return {'Use list' : use_lst, 'Subject list' : subject_lst}

# Define a route /qcm that takes parameters use, subjects, and n to generate a random set of questions based on the given criteria and returns an HTML representation of the selected questions.
@app.get('/qcm')
async def get_questions(use: str, subjects : List[str] = Query(None), n: Optional[int] = 5, username: str = Depends(get_current_user)):
    qcm = df[(df['subject'].isin(subjects)) & (df['use'] == use)].sample(n=n)
    return HTMLResponse(content=qcm.to_html(), status_code=200)

# Create a Pydantic model Question that represents the structure of a new question.
class Question(BaseModel):
    question: str
    subject: str
    correct: str
    use: str
    responseA: str
    responseB: str
    responseC: str
    responseD: str
    remark: str

# Define a route /new_question that allows authenticated users (specifically, the "admin" user) to add a new question to the database. The new question is extracted from the request body, transformed into a DataFrame, and appended to the existing DataFrame.
@app.put('/new_question')
def put_question(question: Question, username: str = Depends(get_current_user)):
    if username == "admin":
        new_question = {
            'question': question.question,
            'subject': question.subject,
            'correct': question.correct,
            'use': question.use,
            'responseA': question.responseA,
            'responseB': question.responseB,
            'responseC': question.responseC,
            'responseD': question.responseD,
            'remark': question.remark
        }
        new_question = pd.DataFrame(pd.json_normalize(new_question))
        global df
        df = pd.concat([df, new_question])
        return df.tail(1)
