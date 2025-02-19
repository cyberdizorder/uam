FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN apt-get update && \
    apt-get install -y tesseract-ocr libtesseract-dev poppler-utils && \
    apt-get install -y tesseract-ocr-pol && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Sprawdzamy faktyczną ścieżkę do tessdata
RUN tesseract --version && \
    ls -la /usr/share/tesseract-ocr/

# Ustawienie zmiennej środowiskowej TESSDATA_PREFIX dla wersji 5
ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/5/tessdata/

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
