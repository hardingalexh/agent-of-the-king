FROM python:3.6-buster
RUN apt-get install ca-certificates
RUN mkdir /code
WORKDIR /code
COPY ./requirements.txt .
RUN pip install -r requirements.txt
RUN pip install --upgrade certifi
