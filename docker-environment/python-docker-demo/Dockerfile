FROM python:3.11-alpine

WORKDIR /app

COPY test_runner.py .
COPY logger.py .
COPY main.py .

ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]