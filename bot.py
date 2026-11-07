import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# BotFather থেকে পাওয়া আপনার টোকেনটি এখানে বসাবেন
BOT_TOKEN = "9079854843:AAHAZP9ZDmtdamKJDw0F13bWdxS12T7x0_0"

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# /start কমান্ড দিলে বট যা উত্তর দিবে
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    await update.message.reply_text(
        f"স্বাগতম, {user_name}!\n\nআপনার বট সফলভাবে চালু হয়েছে। খুব শীঘ্রই এখানে নম্বর নেওয়ার সিস্টেম যুক্ত করা হবে।"
    )

def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    
    print("বট চালু হচ্ছে...")
    application.run_polling()

if __name__ == "__main__":
    main()
