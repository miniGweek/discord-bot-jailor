FROM python:3.10-alpine as build

RUN apk add --update && \
    rm -rf /var/cache/apk/*

WORKDIR /src
COPY . /src

RUN pip install --upgrade pip && \
        pip install -r requirements.txt

CMD [ "python", "main.py" ]