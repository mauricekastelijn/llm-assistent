# llm-assistant

[![CI/CD Pipeline](https://github.com/mauricekastelijn/llm-assistant/actions/workflows/cicd.yml/badge.svg?branch=main)](https://github.com/mauricekastelijn/llm-assistant/actions/workflows/cicd.yml)
[![Dependabot](https://github.com/mauricekastelijn/llm-assistant/actions/workflows/dependabot/dependabot-updates/badge.svg?branch=main)](https://github.com/mauricekastelijn/llm-assistant/actions/workflows/dependabot/dependabot-updates)

Intelligent Personal Assistant application using LLMs and agents, based on the Langchain framework and Ollama backend

## Summary
The llm-assistant project is an intelligent personal assistant application that leverages Large Language Models (LLMs) and agents. It is built using the Langchain framework and Ollama backend. The project aims to provide a modular and scalable solution for personal assistant applications with generative AI capabilities.

## Features
- Web-based frontend for user interaction
   - Including a Gradio-based frontend for interactive user interfaces
- Hosted backend with agentic functionalities using LLMs
- Integration with Langchain framework for building and managing agents
- Local LLM hosting with Ollama in Docker containers
- Data persistence and user-specific state management
- Modular architecture for reusability and extensibility

## Prerequisites
- Docker and Docker Compose installed
- Python 3.12+ installed
- Node.js and npm installed
- Visual Studio Code with Dev Containers extension

## Checking Out and Building the Project
1. Clone the repository:
   ```bash
   git clone https://github.com/mauricekastelijn/llm-assistant.git
   cd llm-assistant
   ```

2. Build and start the Docker containers:
   ```bash
   docker-compose up --build
   ```

3. Access the application:
   - Frontend: http://localhost:8000
   - Gradio Frontend: http://localhost:8000/gradio

## Devcontainer
The project includes a devcontainer configuration for Visual Studio Code. This allows you to develop the project in a consistent environment with all necessary dependencies pre-installed.

To use the devcontainer:
1. Open the project in Visual Studio Code.
2. When prompted, click "Reopen in Container".

## Docker Compose Usage
The project uses Docker Compose to manage multiple containers for the frontend, backend, and Ollama LLM hosting.

### Development
To start the development environment with hot reloading:
```bash
docker-compose -f docker-compose-dev.yml up --build
```

### Production
To start the production environment:
```bash
docker-compose up --build
```

## Hot Reloading in Development
In development mode, the backend container is configured to support hot reloading by mounting volumes into the container. This allows changes to the code to be reflected immediately without restarting the container.

## Secrets Management
Secrets are provided to the containers using Docker secrets. In production builds, secrets are obtained from the environment. In development builds secrets are read from local files for convenience. Refer to docker-compose.yml and docker-compose-dev.yml for details. In both cases the secrets are mounted into the container. The Dockerfile ensures that the the secrets are copied to the correct locations in the container.

## Avoiding SSL Errors Behind Corporate Firewalls
To avoid SSL errors behind corporate firewalls, the project includes the Cisco Umbrella Root CA certificate. This certificate is installed in the Docker containers to ensure secure communication.

For more information, see the Docker documentation on [custom CA certificates](https://docs.docker.com/engine/security/certificates/#understand-custom-ca-certificates).
