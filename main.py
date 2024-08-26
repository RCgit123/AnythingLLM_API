import requests
# import pyrebase
# import firebase_admin
import json
from firebase_admin import credentials, auth
from fastapi import  FastAPI, HTTPException, Depends,File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pathlib import Path
import os
import httpx
from pydantic import BaseModel
# from models import LoginSchema, SignUpSchema



app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
    expose_headers=["*"],
    max_age=36000
)
 

# if not firebase_admin._apps:
#     cred = credentials.Certificate("config.json")
#     firebase_admin.initialize_app(cred)
 
# firebaseConfig = {
#   "apiKey": "AIzaSyBUdZY_AaFjcwWghRvKZBKMrIec6U5HdYk",
#   "authDomain": "llm-authentication-feb08.firebaseapp.com",
#   "projectId": "llm-authentication-feb08",
#   "storageBucket": "llm-authentication-feb08.appspot.com",
#   "databaseURL":"",
#   "messagingSenderId": "335938173864",
#   "appId": "1:335938173864:web:1fcd50dec63f849b44bb9d",
#   "measurementId": "G-4M8XK37Y63"
# }

# firebase=pyrebase.initialize_app(firebaseConfig)
# storage=firebase.storage()

@app.post('/create_workspace')
async def new_workspace(space_name):
    url=f'https://humble-system-x7vjqjvp7pxhpwqx-3001.app.github.dev/api/v1/workspace/new'
    
    headers= {
        "Authorization": "Bearer 73JK2YB-Y7B4GMV-GFSV8Z6-21SMYFW",
        "accept": "application/json"
        }
    
    data={
        "name":f"{space_name}"
    }
    response = requests.post(url,headers=headers,json=data)
    
    if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"{response.text}",
            )
    else:
        return {"message": "**WorkSpace created successfully**"}

@app.get('/workspaces_present')
async def get_workspaces():
    url='https://humble-system-x7vjqjvp7pxhpwqx-3001.app.github.dev/api/v1/workspaces'
       
    headers= {
        "Authorization": "Bearer 73JK2YB-Y7B4GMV-GFSV8Z6-21SMYFW",
        "accept": "application/json"
        }
    response = requests.get(url,headers=headers)
    
    if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"{response.text}",
            )
    else:
        data=json.loads(response.text)
        return data

@app.post('/workspace/slug')
async def get_workspace(slug:str):
    url=f'https://humble-system-x7vjqjvp7pxhpwqx-3001.app.github.dev/api/v1/workspace/{slug}'    
    
       
    headers= {
        "Authorization": "Bearer 73JK2YB-Y7B4GMV-GFSV8Z6-21SMYFW",
        "accept": "application/json"
        }
    
    response = requests.get(url,headers=headers)
    
    if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"{response.text}",
            )
    else:
        data=json.loads(response.text)
        return data
    
@app.delete('/delete/workspace')
async def delete_workspace(slug:str):
    url = f'https://humble-system-x7vjqjvp7pxhpwqx-3001.app.github.dev/api/v1/workspace/{slug}'

    headers = {'accept': '*/*'}
       
    headers= {
        "Authorization": "Bearer 73JK2YB-Y7B4GMV-GFSV8Z6-21SMYFW",
        "accept": '*/*'
        }

    # Send a DELETE request to the API endpoint
    response = requests.delete(url, headers=headers)

    # Check the response status code
    if response.status_code == 200:
        return {'Workspace deleted successfully!'}
    else:
        return {f'Error deleting workspace: {response.status_code} - {response.text}'}

@app.post('/workspace/chats')
async def get_workspace_chat(slug:str):
    url=f'https://humble-system-x7vjqjvp7pxhpwqx-3001.app.github.dev/api/v1/workspace/{slug}/chats'    

    headers= {
        "Authorization": "Bearer 73JK2YB-Y7B4GMV-GFSV8Z6-21SMYFW",
        "accept": "application/json"
        }
    
    response = requests.get(url,headers=headers)
    
    if response.status_code == 200:
            # raise HTTPException(
            #     status_code=response.status_code,
            #     detail=f"{response.text}",
            # )
            data=json.loads(response.text)
            return data
    else:
        print(f"Error fetching data. Status code: {response.status_code}")

@app.post('/QnA')
async def query_and_response(query,slug:str):
    url=f'https://humble-system-x7vjqjvp7pxhpwqx-3001.app.github.dev/api/v1/workspace/{slug}/chat'

 # Define your headers (optional)
    headers = {
    "Authorization": "Bearer 73JK2YB-Y7B4GMV-GFSV8Z6-21SMYFW",
    "Content-Type": "application/json"}
    data = {
    "message": f"{query}",
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


# @app.post('/signup')
# async def create_an_account(user_data:SignUpSchema):
#   email = user_data.email
#   password = user_data.password
  
#   try:
#         user = auth.create_user(
#             email = email,
#             password = password
#         )

#         return JSONResponse(content={"message" : f"User account created successfuly for user {user.uid}"},
#                             status_code= 201
#                )
#   except auth.EmailAlreadyExistsError:
#         raise HTTPException(
#             status_code=400,
#             detail= f"Account already created for the email {email}"
#         )

# @app.post('/login')
# async def create_access_token(user_data:LoginSchema):
    
#     email = user_data.email
#     password = user_data.password

#     try:
#         user = firebase.auth().sign_in_with_email_and_password(
#             email = email,
#             password = password
#         )

#         token = user['idToken']

#         return JSONResponse(
#             content={
#                 "token":token
#             },status_code=200
#         )

#     except:
#         raise HTTPException(
#             status_code=400,detail="Invalid Credentials"
#         )

# @app.post('/ping')
# async def validate_token(request:Request):
#     headers = request.headers
#     jwt = headers.get('authorization')

#     user = auth.verify_id_token(jwt)

#     return user["user_id"] 


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        content= await file.read()
        Path(file.filename).write_bytes(content)
        # storage.child(file.filename).put(file.filename)

        url=   "https://humble-system-x7vjqjvp7pxhpwqx-3001.app.github.dev/api/v1/document/upload"
        headers={
                "Authorization": "Bearer 73JK2YB-Y7B4GMV-GFSV8Z6-21SMYFW",
                "accept": "application/json"
            }
        files = {'file': (file.filename, content, file.content_type)}
        print(file.filename)
        #async with httpx.AsyncClient() as client:
        response = requests.post(url, headers=headers, files=files)

        # Validate response status code
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Error uploading file: {response.text}",
            )
        
        os.remove(file.filename)
        return {"message": "File uploaded successfully"}

    except Exception as e:
        raise HTTPException(status_code=400, detail="File upload failed.")


@app.post("/update_embeddings")
async def update_workspace_embeddings(filename,slug:str):
        url=f'https://humble-system-x7vjqjvp7pxhpwqx-3001.app.github.dev/api/v1/workspace/{slug}/update-embeddings'
        headers={
            "Authorization": "Bearer 73JK2YB-Y7B4GMV-GFSV8Z6-21SMYFW",
                "accept": "application/json"
        }
        file= filename
        docs_url='https://humble-system-x7vjqjvp7pxhpwqx-3001.app.github.dev/api/v1/documents'
        doc_header={
            "Authorization": "Bearer 73JK2YB-Y7B4GMV-GFSV8Z6-21SMYFW",
                "accept": "application/json"
        }
        doc_resp=requests.get(docs_url,headers=doc_header)
        for item in doc_resp.json()['localFiles']['items'][0]['items']:
            if file in item['name']:
                 fileName=item['name']
        data = {
            "adds": [ f"custom-documents/{fileName}"
            ],
            "deletes": [" "]
            
        }
        update_resp=requests.post(url, headers=headers, json=data)
        if update_resp.status_code != 200:
            raise HTTPException(
                status_code=update_resp.status_code,
                detail=f"Error uploading file: {update_resp.text}",
            )
        else:
            return {"message": "Embeddings updated successfully"}
            
@app.get("/docs_list")
async def list_of_docs():
    url="https://humble-system-x7vjqjvp7pxhpwqx-3001.app.github.dev/api/v1/documents"
    headers= {
        "Authorization": "Bearer 73JK2YB-Y7B4GMV-GFSV8Z6-21SMYFW",
        "accept": "application/json"
        }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
    except Exception as exc:
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")

    list = response.json()
    doc_list= list['localFiles']['items'][0]
    doc_names=[]
    for i,item in enumerate(doc_list['items']):
        doc_names.append(item['name'])
    return doc_names

# @app.get("/view_doc")
# async def view_doc(file_name:str):
#     url=storage.child(file_name).get_url(None)
#     return url



if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
    api='https://localhost:8000/view_doc'
    
