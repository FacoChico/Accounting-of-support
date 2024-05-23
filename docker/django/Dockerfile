FROM python:3.10.9-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./backend/requirements.txt .

RUN pip3 install -r requirements.txt

COPY ./backend .

CMD gunicorn -b=0.0.0.0:8000 --workers=4 --threads=2 logisticsAccounting.wsgi:application