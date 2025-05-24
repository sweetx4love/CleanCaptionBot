async def handle_channel_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    post = update.channel_post
    caption = post.caption

    if caption:
        links = list(dict.fromkeys(re.findall(URL_REGEX, caption)))  # ইউনিক লিংক
        
        if links:
            # লিংকগুলিকে "লিংক-১, লিংক-২" ফরম্যাটে ফরম্যাট করুন
            formatted_links = [f"লিংক-{i+1}: {link}" for i, link in enumerate(links)]
            reply_text = "\n".join(formatted_links)  # এক লাইনে একটি লিংক
            
            # মিডিয়া থাকলে রিপোস্ট করুন (অপশনাল)
            if post.photo:
                file_id = post.photo[-1].file_id
                await context.bot.send_photo(
                    chat_id=post.chat_id,
                    photo=file_id,
                    caption=reply_text  # ফরম্যাট করা লিংক
                )
            elif post.video:
                file_id = post.video.file_id
                await context.bot.send_video(
                    chat_id=post.chat_id,
                    video=file_id,
                    caption=reply_text  # ফরম্যাট করা লিংক
                )
            else:
                # শুধু টেক্সট মেসেজ হলে রিপ্লাই দিন
                await post.reply_text(reply_text)

    # মূল মেসেজ ডিলিট করুন (ঐচ্ছিক)
    try:
        await context.bot.delete_message(chat_id=post.chat_id, message_id=post.message_id)
    except Exception as e:
        print("⚠️ মেসেজ ডিলিট করতে সমস্যা:", e)
