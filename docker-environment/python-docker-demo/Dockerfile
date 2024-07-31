FROM python:3.9-alpine
WORKDIR /app
COPY requirements.txt .
RUN apk add --no-cache gcc musl-dev linux-headers && \
    pip install --no-cache-dir -r requirements.txt
COPY app.py .
CMD ["python", "app.py"]