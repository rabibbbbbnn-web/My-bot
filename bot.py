import os
import logging
from threading import Thread
from http.server import HTTPServer, SimpleHTTPRequestHandler
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
)
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

# SMSApp API Key যুক্ত করা হলো
SMSAPP_API_KEY = "sk_ZoM2uldkNxqxsHHKRSab93EAQPKiVTL4fWdU6hQtLiE"

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

# স্থায়ী কি-বোর্ড (Reply Keyboard) যা নিচে সবসময় থাকবে
def get_bottom_reply_keyboard():
    keyboard = [
        [KeyboardButton("📥 Get Number"), KeyboardButton("🔍 Search Number")],
        [KeyboardButton("⚡ Traffic"), KeyboardButton("🛡️ 2FA Online")],
        [KeyboardButton("🎁 Refer"), KeyboardButton("👤 My Profile")],
        [KeyboardButton("🎧 Support")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# সার্ভিস সিলেকশন মেনু
def get_service_markup():
    keyboard = [
        [InlineKeyboardButton("📘 FACEBOOK", callback_data="svc_facebook")],
        [InlineKeyboardButton("💬 WHATSAPP", callback_data="svc_whatsapp")],
        [InlineKeyboardButton("📸 INSTAGRAM", callback_data="svc_instagram")],
        [InlineKeyboardButton("✖️ LETZ", callback_data="svc_letz")],
        [InlineKeyboardButton("❌ Close", callback_data="close_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

# কান্ট্রি সিলেকশন মেনু (উদাহরণস্বরূপ)
def get_country_markup(service):
    keyboard = [
        [InlineKeyboardButton("🇨🇲 Cameroon (24)", callback_data=f"num_{service}_cm"), InlineKeyboardButton("🇱🇸 Lesotho (17)", callback_data=f"num_{service}_ls")],
        [InlineKeyboardButton("🇧🇯 Benin (17)", callback_data=f"num_{service}_bj"), InlineKeyboardButton("🇬🇳 Guinea (13)", callback_data=f"num_{service}_gn")],
        [InlineKeyboardButton("🇦🇲 Armenia (6)", callback_data=f"num_{service}_am"), InlineKeyboardButton("🇹🇬 Togo (2)", callback_data=f"num_{service}_tg")],
        [InlineKeyboardButton("🔙 Back To Services", callback_data="main_get_number")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "✨ **WBE Number Bot** ✨\n\n"
        "সবচেয়ে দ্রুতলয়ে ওটিপি এবং ভার্চুয়াল নাম্বার পাওয়ার বিশ্বস্ত মাধ্যম।"
    )
    await update.message.reply_text(
        welcome_text,
        reply_markup=get_bottom_reply_keyboard(),
        parse_mode="Markdown"
    )

# নিচে থাকা বাটনগুলোর হ্যান্ডলার
async def handle_reply_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == "📥 Get Number":
        await show_services(update)
    elif text == "🔍 Search Number":
        await update.message.reply_text("সার্চ অপশন: অনুগ্রহ করে আপনার কাঙ্ক্ষিত নাম্বার রেঞ্জ লিখুন।")
    elif text == "⚡ Traffic":
        await show_traffic(update)
    elif text == "🛡️ 2FA Online":
        await update.message.reply_text("2FA অনলাইন সার্ভিস: বর্তমানে কোনো সার্ভিস এভেইলেবল নেই।")
    elif text == "🎁 Refer":
        await update.message.reply_text("আপনার রেফারেল লিংক: https://t.me/yourbot?start=ref123\nপ্রতি রেফারেল এ ১০ টাকা বোনাস!")
    elif text == "👤 My Profile":
        user = update.effective_user
        await update.message.reply_text(f"👤 **আপনার প্রোফাইল**\n\nনাম: {user.first_name}\nআইডি: `{user.id}`\nব্যালেন্স: $0.00\nস্ট্যাটাস: Active ✅", parse_mode="Markdown")
    elif text == "🎧 Support":
        keyboard = [[InlineKeyboardButton("💬 Contact Support", url="https://t.me/YourSupportChannel")], [InlineKeyboardButton("❌ Close", callback_data="close_menu")]]
        await update.message.reply_text("যেকোনো প্রয়োজনে আমাদের সাপোর্ট টিমের সাথে যোগাযোগ করুন:", reply_markup=InlineKeyboardMarkup(keyboard))

async def show_services(update, edit=False):
    text = "Select a service:"
    if edit and update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=get_service_markup())
    else:
        await update.message.reply_text(text, reply_markup=get_service_markup())

async def show_traffic(update, edit=False):
    traffic_text = (
        "🔥 **10 Minute LIVE Traffic** 🔥\n\n"
        "📘 **FACEBOOK 63**\n"
        "• CAMEROON : HIGH 🟢\n"
        "• LESOTHO : HIGH 🟢\n\n"
        "💬 **WHATSAPP 18**\n"
        "• MALI : HIGH 🟢\n\n"
        "📸 **INSTAGRAM 11**\n"
        "• ARMENIA : HIGH 🟢\n\n"
        "🕒 *Updated just now*"
    )
    keyboard = [
        [InlineKeyboardButton("🔄 Refresh", callback_data="refresh_traffic")],
        [InlineKeyboardButton("❌ Close", callback_data="close_menu")]
    ]
    if edit and update.callback_query:
        await update.callback_query.edit_message_text(traffic_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
    else:
        await update.message.reply_text(traffic_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("svc_"):
        service = data.split("_")[1]
        await query.edit_message_text(f"Select a country for {service.upper()}:", reply_markup=get_country_markup(service))
    
    elif data.startswith("num_"):
        parts = data.split("_")
        service = parts[1]
        country = parts[2]
        await query.edit_message_text(f"جاری ہے... (Processing)\nআপনার {service.upper()} ({country.upper()}) নাম্বারটি তৈরি হচ্ছে, অনুগ্রহ করে অপেক্ষা করুন।")

    elif data == "main_get_number":
        await show_services(update, edit=True)
    elif data == "refresh_traffic":
        await show_traffic(update, edit=True)
    elif data == "close_menu":
        await query.message.delete()

if __name__ == '__main__':
    server_thread = Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN is missing from environment variables")

    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_reply_keyboard))
    application.add_handler(CallbackQueryHandler(button_callback))
    
    print("বট সফলভাবে চালু হচ্ছে...")
    application.run_polling()
