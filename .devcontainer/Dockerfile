FROM mcr.microsoft.com/devcontainers/base:bullseye

COPY .devcontainers/certs/*.crt /usr/local/share/ca-certificates/

RUN update-ca-certificates