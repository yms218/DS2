from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Static 파일을 제공하기 위한 디렉토리 설정
app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2 템플릿 디렉토리 설정
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def get_home(request: Request):
    # 홈페이지를 렌더링합니다.
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/jupyter/")
async def get_jupyter(request: Request):
    # Jupyter Notebook을 띄우는 페이지를 렌더링합니다.
    return templates.TemplateResponse("jupyter.html", {"request": request})