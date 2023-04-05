FROM python:3.11.2-alpine

COPY scripts/requirements.txt /app/requirements.txt
COPY templates/execution.payload.json /app/templates/execution.payload.json
COPY scripts/entrypoint.sh /usr/bin/entrypoint.sh
COPY scripts/execution.py /usr/bin/execution.py

RUN apk update && \
apk add \
bash

RUN pip install -r /app/requirements.txt && \
rm -rf requirements.txt

WORKDIR /app

ENTRYPOINT [ "bash", "/usr/bin/entrypoint.sh" ]