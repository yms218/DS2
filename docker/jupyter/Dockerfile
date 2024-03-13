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

