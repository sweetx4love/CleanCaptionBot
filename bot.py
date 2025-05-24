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
    await update.message.reply_text("Send")

async def handle_channel_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    post = update.channel_post
    caption = post.caption

    if caption:
        links = list(dict.fromkeys(re.findall(URL_REGEX, caption)))  # ইউনিক লিংক
        
        if links:
            # প্রতিটি লিংকের পর একটি খালি লাইন যোগ করুন
            formatted_links = [f"Link-{i+1}: {link}\n" for i, link in enumerate(links)]
            reply_text = "\n".join(formatted_links)  # লিংকগুলোকে আলাদা লাইনে দেখাবে
            
            # মিডিয়া থাকলে রিপোস্ট করুন
            if post.photo:
                file_id = post.photo[-1].file_id
                await context.bot.send_photo(
                    chat_id=post.chat_id,
                    photo=file_id,
                    caption=reply_text.strip()  # strip() দিয়ে অপ্রয়োজনীয় স্পেস ট্রিম করুন
                )
            elif post.video:
                file_id = post.video.file_id
                await context.bot.send_video(
                    chat_id=post.chat_id,
                    video=file_id,
                    caption=reply_text.strip()
                )
            else:
                # শুধু টেক্সট মেসেজ হলে রিপ্লাই দিন
                await post.reply_text(reply_text.strip())

    # মূল মেসেজ ডিলিট করুন (ঐচ্ছিক)
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
