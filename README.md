""Contexte
Pour cette évaluation, nous allons nous placer dans la peau d'une entreprise qui crée des questionnaires via une application pour Smartphone ou pour navigateur Web. Pour simplifier l'architecture de ces différents produits, l'entreprise veut mettre en place une API. Celle-ci a pour but d'interroger une base de données pour retourner une série de questions.


L'objectif de cette évaluation est donc de créer cette API.

Les données
Notre base de données est représentée par un fichier csv disponible à cette adresse.

Vous pouvez télécharger le jeu de données sur la machine en faisant:

wget https://dst-de.s3.eu-west-3.amazonaws.com/fastapi_fr/questions.csv
On y retrouve les champs suivants:

question: l'intitulé de la question
subject: la catégorie de la question
correct: la liste des réponses correctes
use: le type de QCM pour lequel cette question est utilisée
responseA: réponse A
responseB: réponse B
responseC: réponse C
responseD: la réponse D (si elle existe)
Explorez ce jeu de données pour comprendre ces données

L'API
Sur l'application ou le navigateur Web, l'utilisateur doit pouvoir choisir un type de test (use) ainsi qu'une ou plusieurs catégories (subject). De plus, l'application peut produire des QCMs de 5, 10 ou 20 questions. L'API doit donc être en mesure de retourner ce nombre de questions. Comme l'application doit pouvoir générer de nombreux QCMs, les questions doivent être retournées dans un ordre aléatoire: ainsi, une requête avec les mêmes paramètres pourra retourner des questions différentes.

Les utilisateurs devant avoir créé un compte, il faut que nous soyons en mesure de vérifier leurs identifiants. Pour l'instant l'API utilise une authentification basique, à base de nom d'utilisateur et de mot de passe: la chaîne de caractères contenant Basic username:password devra être passée dans l'en-tête Authorization (en théorie, cette chaîne de caractère devrait être encodée mais pour simplifier l'exercice, on peut choisir de ne pas l'encoder)

Pour les identifiants, on pourra utiliser le dictionnaire suivant:

{
  "alice": "wonderland",
  "bob": "builder",
  "clementine": "mandarine"
}
L'API devra aussi implémenter un point de terminaison pour vérifier que l'API est bien fonctionnelle. Une autre fonctionnalité doit pouvoir permettre à un utilisateur admin dont le mot de passe est 4dm1N de créer une nouvelle question.

Enfin, elle devra être largement documentée et devra renvoyer des erreurs lorsque celle-ci est mal appelée.

Rendus
Les attendus sont un ou plusieurs fichiers Python contenant le code de l'API et un fichier contenant les requêtes à effectuer pour tester l'API. On pourra aussi fournir un fichier requirements.txt listant les librairies à installer. Enfin, vous pouvez fournir un document expliquant les choix d'architecture effectués.

pip freeze > actual_library.txt
pip install -r requirements.txt

Fork https://github.com/fallewi/fast-api
git clone https://github.com/OlivierA59000/fast-api.git 

wget https://dst-de.s3.eu-west-3.amazonaws.com/fastapi_fr/questions.csv

uvicorn main:app --reload
http://localhost:8000/
http://localhost:8000/docs
http://localhost:8000/redoc
http://localhost:8000/openapi.json
curl -X GET http://127.0.0.1:8000/
curl -X GET -i http://127.0.0.1:8000/




git add main.py
git commit -m "Changes"
git push

curl -X GET -i http://127.0.0.1:8000/item/1
curl -X GET -i http://127.0.0.1:8000/?argument1=hello%20world
curl -X GET -i http://127.0.0.1:8000/typed?argument1=1234

curl -X 'POST' -i \
  'http://127.0.0.1:8000/item' \
  -H 'Content-Type: application/json' \
  -d '{
  "itemid": 1234,
  "description": "my object",
  "owner": "Daniel"
}'

curl -X GET -i http://127.0.0.1:8000/headers


# Sur l'application ou le navigateur Web, l'utilisateur doit pouvoir choisir un type de test (use) ainsi qu'une ou plusieurs catégories (subject). De plus, l'application peut produire des QCMs de 5, 10 ou 20 questions. L'API doit donc être en mesure de retourner ce nombre de questions. Comme l'application doit pouvoir générer de nombreux QCMs, les questions doivent être retournées dans un ordre aléatoire: ainsi, une requête avec les mêmes paramètres pourra retourner des questions différentes.

# Les utilisateurs devant avoir créé un compte, il faut que nous soyons en mesure de vérifier leurs identifiants. Pour l'instant l'API utilise une authentification basique, à base de nom d'utilisateur et de mot de passe: la chaîne de caractères contenant Basic username:password devra être passée dans l'en-tête Authorization (en théorie, cette chaîne de caractère devrait être encodée mais pour simplifier l'exercice, on peut choisir de ne pas l'encoder)

# L'API devra aussi implémenter un point de terminaison pour vérifier que l'API est bien fonctionnelle.

# Une autre fonctionnalité doit pouvoir permettre à un utilisateur admin dont le mot de passe est 4dm1N de créer une nouvelle question.

# Enfin, elle devra être largement documentée et devra renvoyer des erreurs lorsque celle-ci est mal appelée.


# api

@app.get('/')
def get_index(argument1):
    return {
        'data': argument1
    }

@app.get('/typed')
def get_typed(argument1: int):
    return {
        'data': argument1 + 1
    }





from typing import Optional

@api.get('/addition')
def get_addition(a: int, b: Optional[int]=None):
    if b:
        result = a + b
    else:
        result = a + 1
    return {
        'addition_result': result
    }

from pydantic import BaseModel
from typing import Optional

class Item(BaseModel):
    itemid: int
    description: str
    owner: Optional[str] = None

@api.post('/item')
def post_item(item: Item):
    return {
        'itemid': item.itemid
    }

@api.get('/users/{userid:int}/name')
def get_user_name(userid):
    try:
        user = list(filter(lambda x: x.get('user_id') == userid, users_db))[0]
        return {'name': user['name']}
    except IndexError:
        return {}

@api.get('/users/{userid:int}/subscription')
def get_user_suscription(userid):
    try:
        user = list(filter(lambda x: x.get('user_id') == userid, users_db))[0]
        return {'subscription': user['subscription']}
    except IndexError:
        return {}

@app.get('/other')
def get_other():
    return {
        'method': 'get',
        'endpoint': '/other'
    }



class Item(BaseModel):
    itemid: int
    description: str
    owner: Optional[Owner] = None
    ratings: List[float]
    available: bool

from fastapi import Header


@app.post('/')
def post_index():
    return {
        'method': 'post',
        'endpoint': '/'
        }

@app.delete('/')
def delete_index():
    return {
        'method': 'delete',
        'endpoint': '/'
        }

@app.put('/')
def put_index():
    return {
        'method': 'put',
        'endpoint': '/'
        }

@app.patch('/')
def patch_index():
    return {
        'method': 'patch',
        'endpoint': '/'
        }