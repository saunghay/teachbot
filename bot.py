import os
import sqlite3
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")

# ================= DB =================
conn = sqlite3.connect("teach.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS teach (
    key TEXT PRIMARY KEY,
    value TEXT
)
""")
conn.commit()

# ================= ADMIN CHECK =================
async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id

    member = await context.bot.get_chat_member(chat_id, user_id)
    return member.status in ["administrator", "creator"]

# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot Active!\nAdmin only can teach me.")

# ================= TEACH =================
async def teach(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await is_admin(update, context):
        await update.message.reply_text("❌ Only admins can teach me!")
        return

    try:
        text = update.message.text.replace("/teach", "").strip()
        key, value = text.split("=", 1)

        key = key.strip().lower()
        value = value.strip()

        cursor.execute("REPLACE INTO teach (key, value) VALUES (?, ?)", (key, value))
        conn.commit()

        await update.message.reply_text(f"✅ Saved:\n{key} → {value}")

    except:
        await update.message.reply_text("❌ Format: /teach hi = Hello")

# ================= AUTO REPLY =================
async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower().strip()

    cursor.execute("SELECT value FROM teach WHERE key = ?", (text,))
    result = cursor.fetchone()

    if result:
        await update.message.reply_text(result[0])

# ================= RUN =================
app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("teach", teach))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

app.run_polling()
