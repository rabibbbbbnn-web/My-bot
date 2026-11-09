import os
import time
import logging
import requests

# ==================== [ CONFIGURATION ] ====================
BOT_TOKEN      = "9079854843:AAHAZP9ZDmtdamKJDw0F13bWdxS12T7x0_0"
ZENEX_API_KEY  = "ZNX_LF178UCH2NIJDSBE0WKJ50LY"
TARGET_CHAT_ID = 8771099641 

ZENEX_ENDPOINT = "https://api.zenexnetwork.com/v1/numsuccess"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ==================== [ FETCH ZENEX OTP ] ====================
def fetch_zenex_otp(endpoint, api_key):
    headers = {
        "mapikey": api_key,
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(endpoint, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        logging.error(f"Error fetching OTP: {e}")
    return None

# ==================== [ SEND TELEGRAM MESSAGE ] ====================
def send_telegram_message(bot_token, chat_id, text):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML'
    }
    try:
        requests.post(url, data=payload, timeout=10)
    except Exception as e:
        logging.error(f"Error sending Telegram message: {e}")

# ==================== [ MAIN LOOP ] ====================
def main():
    logging.info("Bot started and fetching OTPs...")
    while True:
        data = fetch_zenex_otp(ZENEX_ENDPOINT, ZENEX_API_KEY)
        
        if data and 'data' in data and 'otps' in data['data'] and data['data']['otps']:
            for otp_item in data['data']['otps']:
                service = otp_item.get('service', 'Unknown Service')
                number  = otp_item.get('number', 'N/A')
                otp     = otp_item.get('otp', 'No Code')
                country = otp_item.get('country', 'N/A')
                
                message = "🚨 <b>NEW OTP RECEIVED</b> 🚨\n\n"
                message += f"🌐 <b>Service:</b> {service}\n"
                message += f"📱 <b>Number:</b> {number}\n"
                message += f"🌍 <b>Country:</b> {country}\n"
                message += f"🔑 <b>OTP Code:</b> <code>{otp}</code>\n"
                
                send_telegram_message(BOT_TOKEN, TARGET_CHAT_ID, message)
        
        time.sleep(5) # প্রতি ৫ সেকেন্ড পর পর চেক করবে

if __name__ == '__main__':
    main()
