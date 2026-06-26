from fastapi import FastAPI, Form
from fastapi.responses import RedirectResponse
import requests
import os
import resend

app = FastAPI()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
resend.api_key = os.getenv("RESEND_API_KEY")

REDIRECT_URL = "https://popul-etsy-pricing-calc.hf.space" 

@app.post("/submit-email")
async def handle_email(email: str = Form(...)):
    # 1. Fire the notification to Telegram
    message = f"🎉 New Lead Captured: {email}"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": message})
    
    # 2. Send the Automated Welcome Email
    email_html = f"""
    <p>Hey,</p>
    <p>Your margins are about to get a lot clearer.</p>
    <p>You can access your automated Etsy Pricing Calculator right here: <strong><a href="{REDIRECT_URL}">Open The Calculator</a></strong></p>
    <p><em>Pro tip: Bookmark that link. Use it every single time before you publish a new listing so you never accidentally lose money to hidden fees again.</em></p>
    <p>Hit reply if you have any questions - I read every email.</p>
    """
    
    resend.Emails.send({
        "from": "tools@marginandcraft.studio", # Update this once you verify your domain
        "to": email,
        "subject": "You're in! Access your Etsy Pricing Matrix 📈",
        "html": email_html
    })
    
    # 3. Instantly redirect them to the calculator
    return RedirectResponse(url=REDIRECT_URL, status_code=303)
