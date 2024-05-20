import httpx
import requests  # 누락된 requests 임포트
import base64
from pydantic import BaseModel
from urllib.parse import quote
from fastapi import APIRouter, HTTPException, Request
from aiocache import cached, Cache
from aiocache.serializers import JsonSerializer

router = APIRouter()

ACCESS_TOKEN = ''


# 공통 헤더 설정 함수
def get_headers():
    return {
        "Authorization": f"token {ACCESS_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

# 캐싱 데코레이터 사용
@cached(ttl=30000, cache=Cache.MEMORY, serializer=JsonSerializer())
async def fetch_data_with_cache(url: str, headers: dict):
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error fetching data")
        return response.json()
    

async def fetch_data(url: str, headers: dict):
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error fetching data")
        return response.json()


@router.get("/github/repos/{owner}/{repo}")
async def get_github_repo(owner: str, repo: str):
    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = get_headers()
    return await fetch_data_with_cache(url, headers)

@router.get("/github/emojis")
async def get_github_emojis():
    url = "https://api.github.com/emojis"
    headers = get_headers()
    return await fetch_data_with_cache(url, headers)

@router.get("/github/colors")
async def get_github_colors():
    url = "https://raw.githubusercontent.com/ozh/github-colors/master/colors.json"
    headers = {}  # raw.githubusercontent.com은 인증 헤더가 필요 없습니다.
    return await fetch_data_with_cache(url, headers)

@router.get("/models")
async def read_repos():
    url = "https://api.github.com/user/repos"
    headers = get_headers()
    data = await fetch_data(url, headers)
    repos = [{
        "full_name": repo["full_name"],
        "private": repo["private"]
    } for repo in data 
    if repo["owner"]["login"] == "yms218" 
    and repo["fork"] == False ]
    return repos

@router.get("/repos/{owner}/{repo}/commits")
async def get_repo_commits(owner: str, repo: str):
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    headers = get_headers()
    return await fetch_data(url, headers)

async def get_github_repo_tree(owner: str, repo: str):
    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/main?recursive=1"
    headers = get_headers()
    return await fetch_data_with_cache(url, headers)

@router.get("/repos/{owner}/{repo}/tree")
async def read_repo_tree(owner: str, repo: str):
    return await get_github_repo_tree(owner, repo)

async def get_github_file_content(owner: str, repo: str, path: str):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    headers = get_headers()
    return await fetch_data_with_cache(url, headers)

@router.get("/repos/{owner}/{repo}/file")
async def read_file_content(owner: str, repo: str, path: str):
    return await get_github_file_content(owner, repo, path)

@router.get("/github/readme-link")
async def get_github_readme_link(owner: str, repo: str):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/README.md"
    headers = get_headers()
    response = requests.get(url, headers=headers)
    content = response.json()
    readme_url = content.get('html_url', None)

    branch = readme_url.split('/blob/')[1].split('/')[0]
    
    # Create the iframe URL
    iframe_url = f"https://emgithub.com/iframe.html?target=https%3A%2F%2Fgithub.com%2F{owner}%2F{repo}%2Fblob%2F{branch}%2FREADME.md&style=default&type=markdown&showBorder=on&showLineNumbers=on&showFileMeta=on&showFullPath=on&showCopy=on"

    return {"iframe_url": iframe_url}

@router.put("/github/update-readme")
async def update_readme(owner: str, repo: str, request: Request):
    data = await request.json()
    content = data.get("content")
    sha = data.get("sha")

    if not content or not sha:
        raise HTTPException(status_code=400, detail="Content and SHA are required")

    url = f"https://api.github.com/repos/{owner}/{repo}/contents/README.md"
    headers = get_headers()
    payload = {
        "message": "Updating README.md",
        "content": base64.b64encode(content.encode('utf-8')).decode('utf-8'),
        "sha": sha
    }
    response = requests.put(url, json=payload, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error updating README.md")
    return response.json()

class CreateRepoRequest(BaseModel):
    name: str
    description: str = None
    private: bool = False

@router.post("/github/create-repo")
async def create_github_repo(repo: CreateRepoRequest):
    url = "https://api.github.com/user/repos"
    headers = get_headers()
    payload = repo.dict()
    payload['auto_init'] = True  # Automatically create a README file
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        if response.status_code != 201:
            raise HTTPException(status_code=response.status_code, detail="Failed to create repository")
        return response.json()
