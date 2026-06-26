from fastapi import FastAPI, Form
from fastapi.responses import RedirectResponse
import requests
import os

app = FastAPI()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
REDIRECT_URL = "https://popul-etsy-pricing-calc.hf.space" 

@app.post("/submit-email")
async def handle_email(email: str = Form(...)):
    message = f"🎉 New Lead Captured: {email}"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    
    # Fire the message to Telegram
    requests.post(url, json={"chat_id": CHAT_ID, "text": message})
    
    # Instantly redirect them to the calculator
    return RedirectResponse(url=REDIRECT_URL, status_code=303)
