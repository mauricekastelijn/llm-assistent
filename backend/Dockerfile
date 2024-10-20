FROM python:3.12-bookworm AS base

ARG APPNAME=backend
ARG BACKEND_SECRETS=backend-secrets

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install the Cisco Umbrella Root CA certificate
# See # See https://docs.docker.com/engine/network/ca-certs/
COPY res/Cisco_Umbrella_Root_CA.cer /usr/local/share/ca-certificates/Cisco_Umbrella_Root_CA.crt
RUN update-ca-certificates

# Install pip requirements
COPY backend/requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /home/${APPNAME}

COPY backend/backend .

RUN --mount=type=secret,id=${BACKEND_SECRETS} \
    cat /run/secrets/${BACKEND_SECRETS} > secrets/.env

RUN adduser --system --group ${APPNAME}
USER ${APPNAME}

FROM base AS prod

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker", "main:app"]

FROM base AS dev
# Required in case of WSL to trigger uvicorn to reload on file changes
ENV WATCHFILES_FORCE_POLLING=true
CMD ["uvicorn", "--reload", "--host", "0.0.0.0", "--port", "8000", "main:app"]
