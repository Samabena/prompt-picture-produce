from fastapi import FastAPI, UploadFile, Form, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from typing import Optional
import os
from PIL import Image
import io
import requests
import base64

app = FastAPI()

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

@app.post("/process/")
async def process_prompt(
    prompt: str = Form(...),
    image: Optional[UploadFile] = File(None)
):
    image_info = None
    image_content = None
    if image:
        try:
            contents = await image.read()
            img = Image.open(io.BytesIO(contents))
            filename = f"{UPLOAD_DIR}/{image.filename}"
            img.save(filename)
            image_info = f"Image sauvegardée : {filename}"
            # Encoder l'image en base64 pour OpenAI
            buffered = io.BytesIO()
            img_format = img.format if img.format else "PNG"
            img.save(buffered, format=img_format)
            img_b64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
            image_content = {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/{img_format.lower()};base64,{img_b64}"
                }
            }
        except Exception as e:
            return JSONResponse(
                status_code=400,
                content={"error": f"Erreur lors du traitement de l'image: {str(e)}"}
            )

    # Construction des messages pour OpenAI
    if image_content:
        messages = [
            {"role": "system", "content": (
                "Tu es un assistant IA expert en cuisine. "
                "Ton rôle est d'aider les utilisateurs à trouver des idées de recettes ou de plats à cuisiner en fonction des ingrédients qu'ils ont sous la main. "
                "Si la question de l'utilisateur n'est pas liée à la cuisine, tu dois répondre poliment que tu es spécialisé uniquement dans la cuisine, décrire ton rôle, et t'excuser de ne pas pouvoir répondre à d'autres types de questions. "
                "Tu dois toujours répondre en français."
            )},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    image_content
                ]
            }
        ]
    else:
        messages = [
            {"role": "system", "content": (
                "Tu es un assistant IA expert en cuisine. "
                "Ton rôle est d'aider les utilisateurs à trouver des idées de recettes ou de plats à cuisiner en fonction des ingrédients qu'ils ont sous la main. "
                "Si la question de l'utilisateur n'est pas liée à la cuisine, tu dois répondre poliment que tu es spécialisé uniquement dans la cuisine, décrire ton rôle, et t'excuser de ne pas pouvoir répondre à d'autres types de questions. "
                "Tu dois toujours répondre en français."
            )},
            {"role": "user", "content": prompt}
        ]

    # Appel à l'API OpenAI
    try:
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-4o",
            "messages": messages,
            "max_tokens": 512,
            "temperature": 0.7
        }
        openai_response = requests.post(OPENAI_API_URL, headers=headers, json=data, timeout=60)
        openai_response.raise_for_status()
        openai_data = openai_response.json()
        ai_reply = openai_data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        ai_reply = f"Erreur lors de l'appel à OpenAI: {str(e)}"
    # Construction de la réponse
    final_response = ai_reply
    if image_info:
        final_response = f"{image_info}\n\nRéponse IA : {ai_reply}"
    return {"response": final_response}

# Sert index.html à la racine
@app.get("/")
def read_index():
    return FileResponse("index.html")

# Sert les fichiers statiques (images, css, etc.) via /static
app.mount("/static", StaticFiles(directory=".", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 