FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN apt-get update && \
    apt-get install -y tesseract-ocr libtesseract-dev poppler-utils && \
    pip install --no-cache-dir -r requirements.txt

RUN apt-get install -y tesseract-ocr-pol

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
