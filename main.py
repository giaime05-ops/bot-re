import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# --- SERVER FLASK (Keep-Alive per UptimeRobot) ---
app = Flask(__name__)

@app.route('/')
def home():
    return "GOAT Bot is running!", 200

def run_flask():
    # Render imposta automaticamente la variabile PORT
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)

# --- TELEGRAM BOT LOGIC ---
TOKEN = "8825337862:AAEcKHd7oP73eaRmtsegqeRIIZKVSxnnF-U"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    
    text = update.message.text.lower()
    
    # Risponde quando qualcuno scrive "goat"
    if "goat" in text:
        user_name = update.message.from_user.first_name
        await update.message.reply_text(f"Sei il GOAT del giorno 🐐, {user_name}!")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("GOAT-Bot attivo e operativo 🐐!")

def main():
    # Avvia il server Flask in un thread separato
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Avvia il Bot Telegram
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot in ascolto...")
    application.run_polling()

if __name__ == "__main__":
    main()
