import os
import logging
from threading import Thread
from http.server import HTTPServer, SimpleHTTPRequestHandler
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Update

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class HealthCheckHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")

def run_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    server.serve_forever()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    await update.message.reply_text(
        f"স্বাগতম, {user_name}!\nআপনার বট সফলভাবে চালু হয়েছে।"
    )

if __name__ == '__main__':
    server_thread = Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    # Get token from environment variables
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN is missing from environment variables")

    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    
    print("বট চালু হচ্ছে...")
    application.run_polling()
