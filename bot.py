from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import re
import os

TOKEN = os.getenv("TOKEN") or "YOUR_BOT_TOKEN_HERE"
URL_REGEX = r'(https?://[^\s]+)'

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ এখন বট শুধু লিংক রেখে রিপোস্ট করবে এবং মূল পোস্ট ডিলিট করবে।")

# চ্যানেল পোস্ট হ্যান্ডলার
async def handle_channel_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    post = update.channel_post
    caption = post.caption

    # যদি ক্যাপশন থাকে
    if caption:
        links = re.findall(URL_REGEX, caption)

        if links:
            link_only = "\n".join(links)

            # ফটো
            if post.photo:
                file_id = post.photo[-1].file_id
                await context.bot.send_photo(
                    chat_id=post.chat_id,
                    photo=file_id,
                    caption=link_only
                )

            # ভিডিও
            elif post.video:
                file_id = post.video.file_id
                await context.bot.send_video(
                    chat_id=post.chat_id,
                    video=file_id,
                    caption=link_only
                )

    # মেসেজ ডিলিট করা (সব ক্ষেত্রে)
    try:
        await context.bot.delete_message(chat_id=post.chat_id, message_id=post.message_id)
    except Exception as e:
        print("⚠️ মেসেজ ডিলিট করতে সমস্যা:", e)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL & filters.ChatType.CHANNEL, handle_channel_post))

    print("✅ Bot is running...")
    app.run_polling()
