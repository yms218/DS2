# app.py
import markdown
import base64
import mlflow
import requests
import pandas as pd
from schemas import PredictIn, PredictOut
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

def get_model():
    model = mlflow.sklearn.load_model(model_uri="../mlflow/sk_model")
    return model


MODEL = get_model()

class CreateIn(BaseModel):
    name: str
    nickname: str


class CreateOut(BaseModel):
    status: str
    id: int


app = FastAPI()

# User database
USER_DB = {}

# config
NAME_NOT_FOUND = HTTPException(status_code=400, detail="Name not found.")
MLFLOW_API_URL = "http://localhost:5001/api/2.0/mlflow/"
GITHUB_TOKEN = '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'


# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 배포에서는 보다 안전한 설정을 사용하세요
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static 파일을 제공하기 위한 디렉토리 설정
app.mount("/static", StaticFiles(directory="static"), name="static")

# Static 파일을 제공하기 위한 디렉토리 설정
app.mount("/vue", StaticFiles(directory="./windzo/dist"), name="vue")

# Jinja2 템플릿 디렉토리 설정
templates = Jinja2Templates(directory="./windzo/dist")

@app.get("/")
async def vue_home(request: Request):
    # 홈페이지를 렌더링합니다.
    return templates.TemplateResponse("index.html", {"request": request})


params = {
    'run_id': '1f5044a375c64bd3b28a95a93e2ea4e5',
    'path': ''  
}

# fastAPI CRUD
@app.post("/users", response_model=CreateOut)
def create_user(user: CreateIn):
    USER_DB[user.name] = user.nickname
    user_dict = user.dict()
    user_dict["status"] = "success"
    user_dict["id"] = len(USER_DB)
    return user_dict


@app.get("/users")
def read_user(name: str):
    if name not in USER_DB:
        raise NAME_NOT_FOUND
    return {"nickname": USER_DB[name]}


@app.put("/users")
def update_user(name: str, nickname: str):
    if name not in USER_DB:
        raise NAME_NOT_FOUND
    USER_DB[name] = nickname
    return {"status": "success"}


@app.delete("/users")
def delete_user(name: str):
    if name not in USER_DB:
        raise NAME_NOT_FOUND
    del USER_DB[name]
    return {"status": "success"}


@app.post("/predict", response_model=PredictOut)
def predict(data: PredictIn) -> PredictOut:
    df = pd.DataFrame([data.dict()])
    pred = MODEL.predict(df).item()
    return PredictOut(iris_class=pred)

@app.get("/models")
def get_models():
    response = requests.get(MLFLOW_API_URL + 'registered-models/search')
    return response.json()

@app.get("/artifacts")
def get_artifacts():
    response = requests.get(MLFLOW_API_URL + 'artifacts/list', params=params)
    return response.json()


@app.get("/github/{owner}/{repo}/readme")
def get_github_readme(owner: str, repo: str):
    """GitHub 리포지토리의 README 파일 내용을 반환합니다."""
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    url = f"https://api.github.com/repos/{owner}/{repo}/readme"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        readme_data = response.json()
        readme_content = base64.b64decode(readme_data['content']).decode('utf-8')
        
        # Markdown을 HTML로 변환, fenced_code 확장 사용
        html_content = markdown.markdown(readme_content, extensions=['fenced_code', 'codehilite'])
        
        return HTMLResponse(content=html_content, status_code=200)
    else:
        raise HTTPException(status_code=response.status_code, detail="README not found")