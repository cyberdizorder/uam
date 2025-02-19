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
def extract_text_from_pdf(pdf_bytes):
    try:
        # Dodaj parametr lang='pol' do pytesseract
        images = convert_from_bytes(pdf_bytes)
        text = ""
        for image in images:
            text += pytesseract.image_to_string(image, lang='pol', config='--psm 6')
        return text
    except Exception as e:
        print(f"Błąd podczas ekstrakcji tekstu: {str(e)}")
        raise e

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
    print(f"Otrzymano plik: {file.filename}")  # Debugging
    
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Plik musi być w formacie PDF.")
    
    try:
        file_bytes = await file.read()
        print(f"Rozmiar pliku w bajtach: {len(file_bytes)}")  # Debugging
        
        text = extract_text_from_pdf(file_bytes)
        print(f"Wyekstrahowany tekst: {text[:200]}...")  # Debugging
        
        extracted_data = extract_invoice_data(text)
        print(f"Dane z OpenAI: {extracted_data}")  # Debugging
        
        return JSONResponse(content=eval(extracted_data))
    except Exception as e:
        print(f"Wystąpił błąd: {str(e)}")  # Debugging
        raise HTTPException(status_code=500, detail=f"Błąd przetwarzania: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Witaj w API do przetwarzania faktur. Użyj endpointu /invoice z metodą POST aby przetworzyć fakturę."}
