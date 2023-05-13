FROM python:3.10

WORKDIR /src/server

COPY ./requirements-server.txt /src/requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/src/server"

RUN pip install --no-cache-dir --upgrade -r /src/requirements.txt
