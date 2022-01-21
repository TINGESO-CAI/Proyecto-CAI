FROM python:3.10.1-bullseye

WORKDIR /backend

COPY requirements.txt .


RUN python3 -m pip install -r requirements.txt --no-cache-dir


COPY . .


CMD flask db upgrade && python3 -m flask run --host=0.0.0.0


