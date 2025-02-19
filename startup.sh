#!/bin/bash
mkdir -p /app/.apt/usr/share/tesseract-ocr/5/tessdata/
wget -O /app/.apt/usr/share/tesseract-ocr/5/tessdata/pol.traineddata https://github.com/tesseract-ocr/tessdata/raw/main/pol.traineddata 