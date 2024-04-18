from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import FileResponse

app = FastAPI()


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
