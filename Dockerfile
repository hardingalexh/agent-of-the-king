FROM python:3.6-buster
RUN mkdir /code
WORKDIR /code
COPY ./requirements.txt .
RUN pip install -r requirements.txt
RUN pip install -U pyopenssl
ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
