# Dockerfile
FROM jupyter

# 인증서 복사 (선택적, 볼륨 마운트를 사용하는 경우 필요 없음)
COPY openssl/key.pem /etc/ssl/key.pem
COPY openssl/cert.pem /etc/ssl/cert.pem

# Jupyter Notebook 시작 명령어
CMD ["jupyter", "notebook", "--ip", "0.0.0.0", "--allow-root", "--certfile=/etc/ssl/cert.pem", "--keyfile=/etc/ssl/key.pem"]

