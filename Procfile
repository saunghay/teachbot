from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "8634965579:AAFVnyEvgkVD9C-FFQUSXeIOnaO-s8CCqME"

# memory storage (temporary)
memory = {}

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Teach Bot ready 🤖\nUse /teach key = value")

# /teach command
async def teach(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    try:
        data = text.replace("/teach", "").strip()
        key, value = data.split("=", 1)

        key = key.strip().lower()
        value = value.strip()

        memory[key] = value

        await update.message.reply_text(f"✅ Learned:\n{key} → {value}")

    except:
        await update.message.reply_text("❌ Format: /teach hi = Hello")

# auto reply
async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower().strip()

    if text in memory:
        await update.message.reply_text(memory[text])
    else:
        await update.message.reply_text("I don't know this yet 🤖\nTeach me using /teach")

# run bot
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("teach", teach))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

app.run_polling()
