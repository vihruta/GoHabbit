FROM python:3.10.11-alpine3.18

COPY . ./app

WORKDIR ./app

RUN apk add --update --no-cache git

RUN pip3 install -r requirements.txt

CMD python3 -m bot
