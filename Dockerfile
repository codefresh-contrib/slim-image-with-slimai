FROM python:3.11.2-alpine
RUN apk update && \
apk add \
curl
COPY scripts/entrypoint.sh /usr/bin/entrypoint.sh
ENTRYPOINT [ "/usr/bin/entrypoint.sh" ]