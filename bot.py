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

# মূল মেনু ফাংশন (ব্যাক করার জন্য এটি রিইউজ করা হবে)
def get_main_menu_markup():
    keyboard = [
        [
            InlineKeyboardButton("📥 গেট নাম্বার", callback_data="get_number"),
            InlineKeyboardButton("🔍 সার্চ নাম্বার", callback_data="search_number"),
        ],
        [
            InlineKeyboardButton("⚡ লাইভ নাম্বার", callback_data="live_number"),
            InlineKeyboardButton("📊 ট্রাফিক", callback_data="traffic"),
        ],
        [
            InlineKeyboardButton("🔐 2FA অনলাইন", callback_data="two_fa"),
            InlineKeyboardButton("👥 রেফারেল", callback_data="referral"),
        ],
        [
            InlineKeyboardButton("💰 ব্যালেন্স", callback_data="check_balance"),
            InlineKeyboardButton("🏆 লিডারবোর্ড", callback_data="leaderboard"),
        ],
        [
            InlineKeyboardButton("👤 মাই প্রোফাইল", callback_data="my_profile"),
            InlineKeyboardButton("📞 সাপোর্ট", callback_data="support")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    reply_markup = get_main_menu_markup()
    
    welcome_text = (
        f"✨ **স্বাগতম, {user_name}!** ✨\n\n"
        f"নিচের বাটনগুলো থেকে আপনার প্রয়োজনীয় সেবাটি বেছে নিন 👇"
    )
    
    # যদি কমান্ডের মাধ্যমে আসে (message) অথবা ব্যাক বাটন থেকে আসে (callback_query)
    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")
    elif update.callback_query:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(text=welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    # ব্যাক বাটনের কাজ (মেইন মেনুতে ফিরিয়ে নিয়ে যাওয়া)
    if data == "main_menu":
        user_name = update.effective_user.first_name
        welcome_text = (
            f"✨ **স্বাগতম, {user_name}!** ✨\n\n"
            f"নিচের বাটনগুলো থেকে আপনার প্রয়োজনীয় সেবাটি বেছে নিন 👇"
        )
        await query.edit_message_text(text=welcome_text, reply_markup=get_main_menu_markup(), parse_mode="Markdown")
        return

    # প্রতিটি ফিচারের সাথে নিচে একটি করে "🔙 ব্যাক" বাটন যুক্ত করা হলো
    back_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 মূল মেনুতে ফিরে যান", callback_data="main_menu")]])

    if data == "get_number":
        await query.edit_message_text(text="📥 আপনি **'Get Number'** সিলেক্ট করেছেন।\n\n*(এখানে ফেসবুক, ইমু বা টেলিগ্রাম সার্ভিস ও কান্ট্রি সিলেকশনের এপিআই লজিক যুক্ত হবে)*", reply_markup=back_markup, parse_mode="Markdown")
    elif data == "search_number":
        await query.edit_message_text(text="🔍 আপনি **'Search Number'** সিলেক্ট করেছেন।\n\n*(এখানে নাম্বার রেঞ্জ দিয়ে সার্চ করার অপশন থাকবে)*", reply_markup=back_markup, parse_mode="Markdown")
    elif data == "live_number":
        await query.edit_message_text(text="⚡ আপনি **'Live Number'** সিলেক্ট করেছেন।", reply_markup=back_markup, parse_mode="Markdown")
    elif data == "traffic":
        await query.edit_message_text(text="📊 বর্তমান সার্ভার ট্রাফিক স্ট্যাটাস:\n\n• ক্যামেরুন: হাই ট্রাফিক 🔥\n• আর্মেনিয়া/বেনিন: মিডিয়াম ট্রাফিক ⚡\n• ইন্ডিয়া: লো ট্রাফিক 🟢", reply_markup=back_markup, parse_mode="Markdown")
    elif data == "two_fa":
        await query.edit_message_text(text="🔐 আপনি **'2FA Online'** সিলেক্ট করেছেন।\n\n*(এখানে ফেসবুক বা ইনস্টাগ্রামের 2FA কোড বের করার মেথড থাকবে)*", reply_markup=back_markup, parse_mode="Markdown")
    elif data == "referral":
        await query.edit_message_text(text="👥 আপনার রেফারেল লিংক এবং তথ্য দেখতে এখানে অপশন থাকবে।", reply_markup=back_markup, parse_mode="Markdown")
    elif data == "check_balance":
        await query.edit_message_text(text="💰 আপনার একাউন্টের ব্যালেন্স ও উইথড্র অপশন এখানে শো করবে।", reply_markup=back_markup, parse_mode="Markdown")
    elif data == "leaderboard":
        await query.edit_message_text(text="🏆 আজকের টপ ওটিপি রিসিভার ও উইনারদের তালিকা এখানে দেখা যাবে।", reply_markup=back_markup, parse_mode="Markdown")
    elif data == "my_profile":
        await query.edit_message_text(text="👤 আপনার প্রোফাইল বিবরণী এবং স্ট্যাটাস এখানে দেখতে পাবেন।", reply_markup=back_markup, parse_mode="Markdown")
    elif data == "support":
        await query.edit_message_text(text="📞 কোনো সমস্যা হলে সরাসরি অ্যাডমিনের সাথে যোগাযোগ করুন বা সাপোর্ট লিংকে মেসেজ দিন।", reply_markup=back_markup, parse_mode="Markdown")

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
