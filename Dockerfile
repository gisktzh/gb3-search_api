# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10-slim

ENV SSL_KEY_FILE=key.pem
ENV SSL_CERT_FILE=cert.pem

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install & use pipenv
COPY Pipfile Pipfile.lock ./
RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --dev --system --deploy

WORKDIR /app
COPY . /app

# Expose ports
EXPOSE 8000

# Start application
CMD ["sh", "-c", "uvicorn main:gb3_search --ssl-keyfile=/certs/$SSL_KEY_FILE --ssl-certfile=/certs/$SSL_CERT_FILE --host 0.0.0.0 --port 8000"]
