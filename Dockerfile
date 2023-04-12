FROM python:3.9

WORKDIR /app

COPY ./requeriments.txt /app/requeriments.txt

RUN pip install --no-chache-dir --upgrade -r /app/requeriments.txt

COPY . /app