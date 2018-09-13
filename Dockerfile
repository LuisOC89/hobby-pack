FROM python:alpine
MAINTAINER Luis Orozco <humbledore@gmail.com>

# RUN apt-get update -y && \
#     apt-get install -y python-pip python-dev

WORKDIR '/app'

ADD . .

RUN apk add --virtual deps gcc python-dev musl-dev postgresql-dev

RUN pip install -r requirements.txt

RUN pip install python-dotenv

EXPOSE 5433

EXPOSE 3001

# RUN pip install flask
# RUN pip install sqlalchemy
# RUN pip install flask-sqlalchemy

#CMD ["python", "main.py"]