FROM python:3.11.3-alpine

COPY --chown=root:root . /app

RUN pip3 install -r requirements.txt

VOLUME [ "/app/config.yml" ]

EXPOSE 3000

ENTRYPOINT [ "python", "server.py" ]
