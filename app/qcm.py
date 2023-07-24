import pandas as pd
from random import choices

df = pd.read_csv('questions.csv')
questions = choices(list(df), k=10)

print(questions)