from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from googletrans import Translator

app = FastAPI()
translator = Translator()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
        if not istek.q.strip():
            return {"error": "Lütfen bir yazı giriniz."}
        
        sonuc = translator.translate(istek.q, src=istek.source, dest=istek.target)
        
        return {
            "translatedText": sonuc.text,
            "detectedSourceLang": sonuc.src or istek.source  # garanti olsun
        }
    except Exception as e:
        return {"error": str(e)}
