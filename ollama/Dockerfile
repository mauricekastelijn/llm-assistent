FROM ollama/ollama:latest

# Install the Cisco Umbrella Root CA certificate
COPY res/Cisco_Umbrella_Root_CA.cer /usr/local/share/ca-certificates/Cisco_Umbrella_Root_CA.crt
RUN update-ca-certificates
