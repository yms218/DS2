# app.py
import mlflow
import pandas as pd
from schemas import PredictIn, PredictOut
from fastapi import FastAPI, Request, HTTPException
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

# Fail response
NAME_NOT_FOUND = HTTPException(status_code=400, detail="Name not found.")

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