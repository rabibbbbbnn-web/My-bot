import os
import logging
from threading import Thread
from http.server import HTTPServer, SimpleHTTPRequestHandler
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
)
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton

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
    
    # ইমোজিযুক্ত আকর্ষণীয় বাটন ডিজাইন
    keyboard = [
        [
            InlineKeyboardButton("📥 গেট নাম্বার (Get)", callback_data="get_number"),
            InlineKeyboardButton("⚡ লাইভ নাম্বার (Live)", callback_data="live_number"),
        ],
        [
            InlineKeyboardButton("💰 ব্যালেন্স চেক", callback_data="check_balance"),
            InlineKeyboardButton("📞 হেল্প / সাপোর্ট", callback_data="support")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        f"✨ **স্বাগতম, {user_name}!** ✨\n\n"
        f"আপনার প্রয়োজনীয় সার্ভিসটি নিচে থেকে সিলেক্ট করুন 👇"
    )
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "get_number":
        await query.edit_message_text(text="📥 আপনি **'Get Number'** সিলেক্ট করেছেন।\n\n*(এখানে আপনার এপিআই লজিক যুক্ত করা হবে)*", parse_mode="Markdown")
    elif query.data == "live_number":
        await query.edit_message_text(text="⚡ আপনি **'Live Number'** সিলেক্ট করেছেন।\n\n*(এখানে আপনার এপিআই লজিক যুক্ত করা হবে)*", parse_mode="Markdown")
    elif query.data == "check_balance":
        await query.edit_message_text(text="💰 আপনার একাউন্টের ব্যালেন্স চেক করা হচ্ছে...\n\n*(এখানে ব্যালেন্সের এপিআই যুক্ত হবে)*", parse_mode="Markdown")
    elif query.data == "support":
        await query.edit_message_text(text="📞 কোনো সমস্যা হলে অ্যাডমিনের সাথে যোগাযোগ করুন।", parse_mode="Markdown")

if __name__ == '__main__':
    server_thread = Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN is missing from environment variables")

    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_click))
    
    print("বট সফলভাবে চালু হচ্ছে...")
    application.run_polling()
