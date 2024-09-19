FROM python:3.9-slim

WORKDIR /app

COPY main.py .
COPY logger.py .
COPY test_runner.py .

RUN pip install psutil

ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]