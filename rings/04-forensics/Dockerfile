FROM python:3.11-alpine

WORKDIR /app

COPY unlock_daemon.py .
COPY vault/ /vault/

ENV VAULT_DIR=/vault

EXPOSE 80
EXPOSE 8081

CMD ["python", "unlock_daemon.py"]
