import pandas as pd
from typing import Optional
from fastapi.responses import HTMLResponse

from fastapi import FastAPI
app = FastAPI()

df = pd.read_csv('questions.csv')
df = df[df.columns[df.columns != "correct"]]
use_lst = list(df['use'].unique())
subject_lst = list(df['subject'].unique())

@app.get('/')
def get_index():
    return use_lst, subject_lst

@app.get('/qcm')
async def get_questions(use: str, n: Optional[int] = 5):
    qcm = df[(df['use'] == use)].sample(n=n)
    return HTMLResponse(content=qcm.to_html(), status_code=200)

#     qcm = df[(df['subject'].isin([subjects])) & (df['use'] == use)]

# uvicorn qcm:app --reload