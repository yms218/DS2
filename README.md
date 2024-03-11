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

- Docker File 생성
  
  ```
  # Dockerfile
  FROM jupyter
  
  # 인증서 복사 (선택적, 볼륨 마운트를 사용하는 경우 필요 없음)
  COPY openssl/key.pem /etc/ssl/key.pem
  COPY openssl/cert.pem /etc/ssl/cert.pem
  
  # Jupyter Notebook 시작 명령어
  CMD ["jupyter", "notebook", "--ip", "0.0.0.0", "--allow-root", "--certfile=/etc/ssl/cert.pem", "--keyfile=/etc/ssl/key.>
  ```

- Docker Build
  
  ```
  docker build -t jupyter2 .
  ```

- Docker Run
  
  ```
  docker run -it --rm -p 8888:8888 jupyter2
  ```

- Docker container 접근
  
  ```
  docker exec -it <컨테이너ID_또는_이름> /bin/bash
  ```

- Jupyter notebook config 파일 생성
  
  ```
  jupyter notebook --generate-config
  ```

- config 파일 편집
  
  ```
  nano /root/.jupyter/jupyter_notebook_config.py
  
  
  c = get_config()  #noqa
  c.NotebookApp.tornado_settings = {
          'headers':{
                  'Content-Security-Policy':"frame-ancestors * 'self' "
          }
  }
  ```

- [Docker 활용하여 FastAPI + Nginx 배포 :: Like Sherlock Data Scientist](https://richdad-project.tistory.com/96)

Nginx 설치

- sudo apt-get install nginx

- FastAPI와 Nginx 연동을 위한 Config 파일 작성
  
      server {
       listen 80;
       server_name localhost;
          location / {
              proxy_pass http://localhost:8000;
              proxy_set_header Host $host;
              proxy_set_header X-Real-IP $remote_addr;
              proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
              proxy_set_header X-Forwarded-Proto $scheme;
          }
      
          location /jupyter/ {
              proxy_pass http://localhost:8888; # Jupyter Notebook 서버 주소
              proxy_set_header Host $host;
              proxy_set_header X-Real-IP $remote_addr;
              proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
              proxy_set_header X-Forwarded-Proto $scheme;
      
              # CSP 헤더 설정 예제
              add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline';";
          }
      }

- sites-available의 fastapi.conf 파일을 sites-enabled에 심볼릭 링크 생성
  
  ```
  sudo ln -s /etc/nginx/sites-available/fastapi.conf /etc/nginx/sites-enabled/fastapi.conf
  ```
  
  
