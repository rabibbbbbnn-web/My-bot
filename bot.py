
import os
import logging
from threading import Thread
from http.server import HTTPServer, SimpleHTTPRequestHandler
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Update

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Simple HTTP handler for port binding
class HealthCheckHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")

def run_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    server.serve_forever()

# Command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    await update.message.reply_text(
        f"স্বাগতম, {user_name}!\nআপনার বট সফলভাবে চালু হয়েছে।"
    )

if __name__ == '__main__':
    # Start web server in a separate thread
    server_thread = Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    # Initialize Telegram Bot
    BOT_TOKEN = "9079854843:AAHAZP9ZDmtdamKJDw0F13bWdxS12T7x0_0"
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    
    print("বট চালু হচ্ছে...")
    application.run_polling()


