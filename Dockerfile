FROM python:alpine

# RUN apt-get update -y && \
#     apt-get install -y python-pip python-dev

WORKDIR '/app'

COPY . .

RUN pip install flask
RUN pip install sqlalchemy
RUN pip install flask-sqlalchemy

CMD ["python", "main.py"]