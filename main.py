from fastapi import FastAPI
from pydantic import BaseModel
from googletrans import Translator
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
translator = Translator()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # geçici olarak herkese açık (güvenli değilse sonra sınırlarız)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CeviriIstegi(BaseModel):
    q: str
    source: str
    target: str

@app.post("/translate")
def ceviri_yap(istek: CeviriIstegi):
    try:
        # Boş metin kontrolü
        if not istek.q.strip():
            return {"error": "Lütfen bir yazı giriniz."}

        sonuc = translator.translate(istek.q, src=istek.source, dest=istek.target)
        return {"translatedText": sonuc.text}
    except Exception as e:
        return {"error": str(e)}
