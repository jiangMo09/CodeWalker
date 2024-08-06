FROM python:3.9-slim

RUN apt-get update && apt-get install -y git

WORKDIR /app

COPY start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 8000

ENTRYPOINT ["/start.sh"]