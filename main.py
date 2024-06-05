import requests
import pprint
import json
import pyrebase
import firebase_admin
from firebase_admin import credentials, auth
from fastapi import  FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from pydantic import BaseModel
from models import LoginSchema, SignUpSchema



app=FastAPI(docs_url="/")
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
    expose_headers=["*"],
    max_age=36000
)
class ChatParams(BaseModel):
    query:str
    spacename:str    

if not firebase_admin._apps:
    cred = credentials.Certificate("llm-authentication-feb08-firebase-adminsdk-apofp-652800e86b.json")
    firebase_admin.initialize_app(cred)
 
firebaseConfig = {
  "apiKey": "AIzaSyBUdZY_AaFjcwWghRvKZBKMrIec6U5HdYk",
  "authDomain": "llm-authentication-feb08.firebaseapp.com",
  "projectId": "llm-authentication-feb08",
  "storageBucket": "llm-authentication-feb08.appspot.com",
  "databaseURL":"",
  "messagingSenderId": "335938173864",
  "appId": "1:335938173864:web:1fcd50dec63f849b44bb9d",
  "measurementId": "G-4M8XK37Y63"
}

firebase=pyrebase.initialize_app(firebaseConfig)

@app.post('/QnA')
async def query_and_response(params:ChatParams):
    url=f'http://localhost:3001/api/v1/workspace/{params.spacename}/chat'

 # Define your headers (optional)
    headers = {
    "Authorization": "Bearer G78DPME-1TCMACH-HYMPVDY-71KX4WT",
    "Content-Type": "application/json"}
    data = {
    "message": f"{params.query}",
    "mode": "query"
    }
    response = requests.post(url, headers=headers, json=data)
    ans=response.json()
     # Check the response
    if response.status_code==200:
        texts = []
        for item in ans['sources']:
            texts.append(item['text'])
        result={'textResponse':ans['textResponse'],
                'Citations':texts}
        return result
    else:
        return {response.status_code,"Request Failed!! try again"}


@app.post('/signup')
async def create_an_account(user_data:SignUpSchema):
  email = user_data.email
  password = user_data.password
  
  try:
        user = auth.create_user(
            email = email,
            password = password
        )

        return JSONResponse(content={"message" : f"User account created successfuly for user {user.uid}"},
                            status_code= 201
               )
  except auth.EmailAlreadyExistsError:
        raise HTTPException(
            status_code=400,
            detail= f"Account already created for the email {email}"
        )

@app.post('/login')
async def create_access_token(user_data:LoginSchema):
    
    email = user_data.email
    password = user_data.password

    try:
        user = firebase.auth().sign_in_with_email_and_password(
            email = email,
            password = password
        )

        token = user['idToken']

        return JSONResponse(
            content={
                "token":token
            },status_code=200
        )

    except:
        raise HTTPException(
            status_code=400,detail="Invalid Credentials"
        )

@app.post('/ping')
async def validate_token(request:Request):
    headers = request.headers
    jwt = headers.get('authorization')

    user = auth.verify_id_token(jwt)

    return user["user_id"]







if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)