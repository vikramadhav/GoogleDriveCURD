#Dockerfile
FROM python:alpine3.8

RUN mkdir /application
WORKDIR /application

# Upgrade pip
RUN pip install --upgrade pip
# Update
COPY . /application
COPY ./config.json /application/config.json
COPY ./credentials.json /application/credentials.json


RUN pip install -r /application/requirement.txt

CMD [ "python", "main.py" ]