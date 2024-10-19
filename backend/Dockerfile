FROM python:3.12-bookworm AS base

ARG APPNAME=backend

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install the Cisco Umbrella Root CA certificate
COPY res/Cisco_Umbrella_Root_CA.cer /usr/local/share/ca-certificates/Cisco_Umbrella_Root_CA.crt
RUN update-ca-certificates

# Install pip requirements
COPY backend/requirements.txt .
RUN python -m pip install -r requirements.txt

RUN adduser --system --group ${APPNAME}
USER ${APPNAME}

WORKDIR /home/${APPNAME}

COPY backend/backend .

FROM base AS prod

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker", "main:app"]

FROM base AS dev
# Required in case of WSL to trigger uvicorn to reload on file changes
ENV WATCHFILES_FORCE_POLLING=true
CMD ["uvicorn", "--reload", "--host", "0.0.0.0", "--port", "8000", "main:app"]
