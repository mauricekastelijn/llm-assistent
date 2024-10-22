FROM mcr.microsoft.com/devcontainers/python:3.12

# Install the Cisco Umbrella Root CA certificate
# See # See https://docs.docker.com/engine/network/ca-certs/
COPY res/Cisco_Umbrella_Root_CA.cer /usr/local/share/ca-certificates/Cisco_Umbrella_Root_CA.crt
RUN update-ca-certificates

# Install backend requirements
COPY backend/requirements.txt .
RUN python -m pip install -r requirements.txt
