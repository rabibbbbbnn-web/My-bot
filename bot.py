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

API_SETTINGS = {
    "vortex_api": "সংযুক্ত করা হয়নি ❌"
}

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

def get_admin_menu_markup():
    keyboard = [
        [
            InlineKeyboardButton("🔑 ভোল্টেক্স এপিআই সেটআপ", callback_data="set_vortex_api"),
            InlineKeyboardButton("📊 লিডারবোর্ড ম্যানেজমেন্ট", callback_data="admin_leaderboard"),
        ],
        [
            InlineKeyboardButton("📢 ব্রডকাস্ট মেসেজ", callback_data="admin_broadcast"),
            InlineKeyboardButton("👥 ইউজার ইনফো", callback_data="admin_users"),
        ],
        [
            InlineKeyboardButton("⚙️ সিস্টেম সেটিং", callback_data="admin_settings"),
            InlineKeyboardButton("🔄 সুইচ ডিজাইন", callback_data="admin_switch_design"),
        ],
        [
            InlineKeyboardButton("🔙 মূল মেনুতে ফিরে যান", callback_data="main_menu")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    reply_markup = get_main_menu_markup()
    welcome_text = f"✨ **স্বাগতম, {user_name}!** ✨\n\nনিচের বাটনগুলো থেকে আপনার প্রয়োজনীয় সেবাটি বেছে নিন 👇"
    
    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")
    elif update.callback_query:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(text=welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = get_admin_menu_markup()
    admin_text = f"👑 **স্বাগতম, অ্যাডমিন প্যানেলে!** 👑\n\nবর্তমান এপিআই স্ট্যাটাস: `{API_SETTINGS['vortex_api']}`\n\nনিচের অপশনগুলো থেকে আপনার বটের সবকিছু নিয়ন্ত্রণ করুন 👇"
    
    if update.message:
        await update.message.reply_text(admin_text, reply_markup=reply_markup, parse_mode="Markdown")
    elif update.callback_query:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(text=admin_text, reply_markup=reply_markup, parse_mode="Markdown")

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    
    if data == "main_menu":
        await start(update, context)
        return
    elif data == "admin_menu":
        await admin_panel(update, context)
        return

    if data == "set_vortex_api":
        API_SETTINGS['vortex_api'] = "সফলভাবে সংযুক্ত ✅ (Active Key)"
        back_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 অ্যাডমিন প্যানেলে ফিরুন", callback_data="admin_menu")]])
        await query.edit_message_text(text=f"🔑 **ভোল্টেক্স এপিআই প্যানেল**\n\nআপনার এপিআই কি সফলভাবে যুক্ত করা হয়েছে!\nবর্তমান স্ট্যাটাস: `{API_SETTINGS['vortex_api']}`", reply_markup=back_markup, parse_mode="Markdown")
        return
    elif data == "admin_leaderboard":
        back_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 অ্যাডমিন প্যানেলে ফিরুন", callback_data="admin_menu")]])
        await query.edit_message_text(text="📊 **লিডারবোর্ড ম্যানেজমেন্ট**\n\n• অটো রিওয়ার্ড: অন\n• টপ কাউন্ট: ১৫ জন\n• থিম: ডার্ক", reply_markup=back_markup, parse_mode="Markdown")
        return
    elif data == "admin_broadcast":
        back_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 অ্যাডমিন প্যানেলে ফিরুন", callback_data="admin_menu")]])
        await query.edit_message_text(text="📢 **ব্রডকাস্ট সিস্টেম**\n\nসকল ইউজারের কাছে মেসেজ পাঠানোর অপশন এখানে কাজ করবে।", reply_markup=back_markup, parse_mode="Markdown")
        return
    elif data == "admin_users":
        back_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 অ্যাডমিন প্যানেলে ফিরুন", callback_data="admin_menu")]])
        await query.edit_message_text(text="👥 **ইউজার ইনফো**\n\nসকল ইউজারের ডাটা ফাইল আকারে ডাউনলোড করার সিস্টেম।", reply_markup=back_markup, parse_mode="Markdown")
        return
    elif data == "admin_settings":
        back_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 অ্যাডমিন প্যানেলে ফিরুন", callback_data="admin_menu")]])
        await query.edit_message_text(text="⚙️ **সিস্টেম সেটিং**\n\nফোর্স জয়েন চ্যানেল এবং এডমিন ম্যানেজমেন্ট কন্ট্রোল।", reply_markup=back_markup, parse_mode="Markdown")
        return
    elif data == "admin_switch_design":
        back_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 অ্যাডমিন প্যানেলে ফিরুন", callback_data="admin_menu")]])
        await query.edit_message_text(text="🔄 **সুইচ ডিজাইন**\n\nবটের লুক ও ডিজাইন পরিবর্তনের অপশন।", reply_markup=back_markup, parse_mode="Markdown")
        return

    back_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 মূল মেনুতে ফিরে যান", callback_data="main_menu")]])

    if data == "get_number":
        await query.edit_message_text(text=f"📥 আপনি **'Get Number'** সিলেক্ট করেছেন।\n\nএপিআই স্ট্যাটাস: {API_SETTINGS['vortex_api']}", reply_markup=back_markup, parse_mode="Markdown")
    elif data == "search_number":
        await query.edit_message_text(text="🔍 আপনি **'Search Number'** সিলেক্ট করেছেন।", reply_markup=back_markup, parse_mode="Markdown")
    elif data == "live_number":
        await query.edit_message_text(text="⚡ আপনি **'Live Number'** সিলেক্ট করেছেন।", reply_markup=back_markup, parse_mode="Markdown")
    elif data == "traffic":
        await query.edit_message_text(text="📊 বর্তমান সার্ভার ট্রাফিক স্ট্যাটাস:\n\n• ক্যামেরুন: হাই ট্রাফিক 🔥\n• আর্মেনিয়া/বেনিন: মিডিয়াম ট্রাফিক ⚡\n• ইন্ডিয়া: লো ট্রাফিক 🟢", reply_markup=back_markup, parse_mode="Markdown")
    elif data == "two_fa":
        await query.edit_message_text(text="🔐 আপনি **'2FA Online'** সিলেক্ট করেছেন।", reply_markup=back_markup, parse_mode="Markdown")
    elif data == "referral":
        await query.edit_message_text(text="👥 আপনার রেফারেল লিংক এবং তথ্য এখানে থাকবে।", reply_markup=back_markup, parse_mode="Markdown")
    elif data == "check_balance":
        await query.edit_message_text(text="💰 আপনার একাউন্টের ব্যালেন্স ও উইথড্র অপশন।", reply_markup=back_markup, parse_mode="Markdown")
    elif data == "leaderboard":
        await query.edit_message_text(text="🏆 আজকের টপ ওটিপি রিসিভার ও উইনারদের তালিকা।", reply_markup=back_markup, parse_mode="Markdown")
    elif data == "my_profile":
        await query.edit_message_text(text="👤 আপনার প্রোফাইল বিবরণী।", reply_markup=back_markup, parse_mode="Markdown")
    elif data == "support":
        await query.edit_message_text(text="📞 সরাসরি অ্যাডমিনের সাথে যোগাযোগ বা সাপোর্ট লিংক।", reply_markup=back_markup, parse_mode="Markdown")

if __name__ == '__main__':
    server_thread = Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN is missing from environment variables")

    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("admin", admin_panel))
    application.add_handler(CallbackQueryHandler(button_click))
    
    print("বট সফলভাবে চালু হচ্ছে...")
    application.run_polling()
