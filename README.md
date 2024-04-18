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
  
  # 패키지 리스트 업데이트 및 nano 텍스트 편집기 설치
  USER root
  RUN apt-get update && apt-get install -y nano
  
  # Jupyter Notebook 설정 파일 생성 및 수정
  RUN jupyter notebook --generate-config && \
      echo "c.NotebookApp.tornado_settings = {" >> /root/.jupyter/jupyter_notebook_config.py && \
      echo "    'headers': {" >> /root/.jupyter/jupyter_notebook_config.py && \
      echo "        'Content-Security-Policy': \"frame-ancestors * 'self' \"" >> /root/.jupyter/jupyter_notebook_config.py && \
      echo "    }" >> /root/.jupyter/jupyter_notebook_config.py && \
      echo "}" >> /root/.jupyter/jupyter_notebook_config.py && \
      echo "c.NotebookApp.token = ''" >> /root/.jupyter/jupyter_notebook_config.py && \
      echo "c.NotebookApp.password = ''" >> /root/.jupyter/jupyter_notebook_config.py
  
  # Jupyter Notebook 시작 명령어
  CMD ["jupyter", "notebook", "--ip", "0.0.0.0", "--allow-root"]
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
  
  jupyter notebook password # 비밀번호 생성
  
  nano /root/.jupyter/jupyter_server_config.json
  
  c = get_config()  #noqa
  c.NotebookApp.tornado_settings = {
          'headers':{
                  'Content-Security-Policy':"frame-ancestors * 'self' "
          }
  }
  c.NotebookApp.token=''
  c.NotebookApp.password=''
  ```

- 

- [Docker 활용하여 FastAPI + Nginx 배포 :: Like Sherlock Data Scientist](https://richdad-project.tistory.com/96)

FastAPI - Vue.js 연동

- vue.config.js 파일 설정 
  
  public path를 vue로 추가해준다
  
  ```
  const { defineConfig } = require('@vue/cli-service');
  module.exports = defineConfig({
    transpileDependencies: true,
    publicPath: process.env.NODE_ENV === 'production' ? '/vue/' : '/'
  });
  ```
