FROM ollama/ollama

# Install curl
RUN apt update && apt install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /

COPY start.sh start.sh

COPY modelfiles modelfiles

WORKDIR /modelfiles

WORKDIR /

RUN chmod +x /start.sh

EXPOSE 11434

ENTRYPOINT [ "/start.sh" ]