FROM python:3.11-alpine
WORKDIR /app
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY *.py .
CMD ["python", "main.py"]