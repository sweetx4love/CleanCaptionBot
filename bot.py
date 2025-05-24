from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
import re
import os

TOKEN = os.getenv("TOKEN") or "YOUR_BOT_TOKEN_HERE"
URL_REGEX = r'(https?://[^\s]+)'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome")

async def handle_channel_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    post = update.channel_post
    caption = post.caption

    if caption:
        links = list(dict.fromkeys(re.findall(URL_REGEX, caption)))
        
        if links:
            formatted_links = [f"লিংক-{i+1}: {link}" for i, link in enumerate(links)]
            reply_text = "\n".join(formatted_links)

            if post.photo:
                file_id = post.photo[-1].file_id
                await context.bot.send_photo(
                    chat_id=post.chat_id,
                    photo=file_id,
                    caption=reply_text
                )
            elif post.video:
                file_id = post.video.file_id
                await context.bot.send_video(
                    chat_id=post.chat_id,
                    video=file_id,
                    caption=reply_text
                )
            else:
                await post.reply_text(reply_text)

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
