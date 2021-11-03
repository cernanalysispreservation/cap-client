FROM python:3.8-slim-buster

COPY . /code

RUN pip3 install --no-cache-dir -e /code

ENTRYPOINT [ "cap-client" ]
