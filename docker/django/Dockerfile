FROM python:3.10.9-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./backend/requirements.txt .

RUN pip3 install -r requirements.txt

COPY ./backend .

RUN python3 manage.py makemigrations
RUN python3 manage.py migrate

CMD gunicorn -b=0.0.0.0:8000 logisticsAccounting.wsgi:application