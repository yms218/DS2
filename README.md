# DS2

DS2 12th Project

Airflow 설치 (WSL2 + docker 환경)

- Windows WSL2 설치 - [Windows 10에 WSL2 설치하기](https://hkim-data.tistory.com/17)

- Docker 설치 - [[Docker] windows에 Docker 설치하기 (tistory.com)](https://hkim-data.tistory.com/16)

Jupyter notebook(Docker Image 다운로드 후 컨테이너 실행) - [[Docker] 도커에서 주피터 노트북 원격 접속 방법](https://yeko90.tistory.com/entry/how-to-run-jupyter-docker)

- 예제용 도커 이미지
  
  ```
  docker pull pytorch/pytorch
  
  docker run --rm -it pytorch/pytorch
  
  pip install jupyter
  
  docker ps # 컨테이너 확인 
  
  docker commit CONTAINER_ID
  
  docker images # 생성된 이미지 확인
  
  docker run -it --rm -p 5000:8888 jupyter
  
  jupyter notebook --ip 0.0.0.0 --allow-root
  ```

- fastapi 사용을 위한 라이브러리 설치
  
  ```
  pip install fastapi uvicorn jinja2
  
  uvicorn main:app --reload # fastapi app 실행
  ```

- Https로 jupyter notebook 접근 (OpenSSL) : [[ Downloads ] - /source/index.html](https://www.openssl.org/source/)
  
  ```
  openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365
  
  uvicorn main:app --reload --ssl-keyfile=D:\\web\\openssl\\key.pem --ssl-certfile=D:\\web\\openssl\\cert.pem
  ```

```
- Docker File 생성

```dockerfile
# Dockerfile
FROM jupyter

# 인증서 복사 (선택적, 볼륨 마운트를 사용하는 경우 필요 없음)
COPY openssl/key.pem /etc/ssl/key.pem
COPY openssl/cert.pem /etc/ssl/cert.pem

# Jupyter Notebook 시작 명령어
CMD ["jupyter", "notebook", "--ip", "0.0.0.0", "--allow-root", "--certfile=/etc/ssl/cert.pem", "--keyfile=/etc/ssl/key.>
```

- Docker build : docker build -t jupyter2 .
- docker run -it --rm -p 5000:8888 jupyter2
- docker exec -it <컨테이너ID_또는_이름> /bin/bash
- jupyter notebook --generate-config
- nano /root/.jupyter/jupyter_notebook_config.py         
