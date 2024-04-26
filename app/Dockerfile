# 일부 수정이 필요

FROM amd64/python:3.9-slim

WORKDIR /usr/app

RUN pip install -U pip \
    && pip install "fastapi[all]"

COPY crud_pydantic.py crud_pydantic.py

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]