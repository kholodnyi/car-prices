FROM python:3.10

WORKDIR /src

COPY ./requirements.txt /src/requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/src"

RUN pip install --no-cache-dir --upgrade -r /src/requirements.txt
