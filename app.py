from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import pytesseract
from pdf2image import convert_from_bytes
import re
import openai
import os

app = FastAPI()

# Konfiguracja klucza OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Funkcja do ekstrakcji tekstu z PDF
def extract_text_from_pdf(file_bytes):
    images = convert_from_bytes(file_bytes)
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img, lang='pol')
    return text

# Funkcja do ekstrakcji danych za pomocą OpenAI API
def extract_invoice_data(text):
    prompt = f"""
    Tekst faktury: "{text}"
    Ekstrahuj następujące dane:
    - Numer NIP
    - Adres sprzedawcy
    - Łączna kwota brutto

    Wynik w formacie JSON:
    """

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    
    data = response.choices[0].text.strip()
    return data

# Endpoint do przetwarzania faktur
@app.post("/invoice")
async def process_invoice(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Plik musi być w formacie PDF.")
    
    file_bytes = await file.read()
    text = extract_text_from_pdf(file_bytes)
    extracted_data = extract_invoice_data(text)
    
    return JSONResponse(content=eval(extracted_data))

@app.get("/")
async def root():
    return {"message": "Witaj w API do przetwarzania faktur. Użyj endpointu /invoice z metodą POST aby przetworzyć fakturę."}
