# Dockerfile
FROM jupyter

# 패키지 리스트 업데이트 및 nano 텍스트 편집기 설치
USER root
RUN apt-get update && apt-get install -y nano

# Jupyter Notebook 시작 명령어
CMD ["jupyter", "notebook", "--ip", "0.0.0.0", "--allow-root"]

