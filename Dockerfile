FROM python:alpine

WORKDIR '/app'

ADD . .

RUN apk add --virtual deps gcc python-dev musl-dev postgresql-dev

RUN pip install -r requirements.txt

EXPOSE 8001

# To run in prod environment
CMD gunicorn main:app --bind 0.0.0.0:8001 --reload