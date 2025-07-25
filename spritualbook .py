from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

TOKEN = "8243278603:AAGw58vbb3LyPrFVvQ5hyeJtC2WrF0knw3k"
REQUIRED_CHANNEL = "spritualbooks2"  # Corrected the typo
REQUIRED_GROUP = "spiritualbooks3"      # without @

TOPIC_BUTTONS = [
    ("ስለ ፀጋ", "grace"),
    ("ስለ እምነት", "faith"),
    ("ስለ አማኝ ምልልስ", "repentance"),
    ("የቤተክርስቲያን ታሪክ", "history"),
    ("የኦርቶዶክስ �ስተምህሮት", "orthodox"),
    ("የonly Jesus አስተምህሮት", "only_jesus"),
    ("የሙስልም አስተምህሮት", "muslim"),
    ("የጅሆቫ ዊትኔስ አስተምህሮት", "jehovah"),
    ("እና ሌሎችም", "others")
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    bot = context.bot
    try:
        ch = await bot.get_chat_member(f"@spritualbooks2", user_id)
        gp = await bot.get_chat_member(f"@spiritualbooks3", user_id)
        if ch.status not in ['member', 'administrator', 'creator'] or gp.status not in ['member', 'administrator', 'creator']:
            raise Exception("Not joined")
    except:
        keyboard = [
            [InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/spritualbooks2")],
            [InlineKeyboardButton("👥 Join Group", url=f"https://t.me/spiritualbooks3")],
            [InlineKeyboardButton("✅ I've Joined", callback_data="check_subs")]
        ]
        await update.message.reply_text("👋 Welcome to our bot! Please join our channel and group:", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    await send_main_menu(update, context)

async def check_subs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    bot = context.bot
    try:
        ch = await bot.get_chat_member(f"@spritualbooks2", user_id)
        gp = await bot.get_chat_member(f"@spiritualbooks3", user_id)
        if ch.status in ['member', 'administrator', 'creator'] and gp.status in ['member', 'administrator', 'creator']:
            await query.edit_message_text("✅ You're verified!")
            await send_main_menu(query, context)
        else:
            await query.edit_message_text("❌ Please join both channel and group.")
    except:
        await query.edit_message_text("⚠️ Could not verify. Try again.")

async def send_main_menu(update, context):
    keyboard = []
    row = []
    for i, (label, data) in enumerate(TOPIC_BUTTONS):
        row.append(InlineKeyboardButton(label, callback_data=f"topic_{data}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    if hasattr(update, 'message'):
        await update.message.reply_text("📚 Choose a topic:", reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.edit_message_text("📚 Choose a topic:", reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    topic = query.data.replace("topic_", "")

    topic_messages = {
        "grace": "📘 ስለ ፀጋ ትምህርት፡ \nhttps://t.me/sletsega",
        "faith": "📗 ስለ እምነት ትምህርት፡ \nhttps://t.me/sleemnet",
        "repentance": "📙 ስለ አማኝ ምልልስ፡ \nhttps://t.me/+WI_SVcOsfMFhOWQ0",
        "history": "📖 የቤተክርስቲያን ታሪክ፡ \nhttps://t.me/+lHbscvaZ8RQ1ZGI0",
        "orthodox": "⛪ የኦርቶዶክስ አስተምህሮት፡ \nhttps://t.me/+eCvQG7mxqnc4NDQ0",
        "only_jesus": "✝️ የOnly Jesus አስተምህሮት፡ \nhttps://t.me/+8P0UXfEvAaBkOTRk",
        "muslim": "☪️ የሙስልም አስተምህሮት፡ \nhttps://t.me/+N5uzqnBaovBlNzg8",
        "jehovah": "🕍 የጅሆቫ Witnesses አስተምህሮት፡ \nhttps://t.me/+TY8kqxsK07tiOGRk",
        "others": "📚 ሌሎች አስተምህሮቶች፡ \nhttps://t.me/+phmJC4BUVKMxMjU8"
    }

    msg = topic_messages.get(topic, "❗ Not found.")
    await query.message.reply_text(msg)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_subs, pattern="check_subs"))
    app.add_handler(CallbackQueryHandler(handle_topic, pattern="topic_.*"))
    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()