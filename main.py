import os
from datetime import date
from threading import Thread
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# === MINI WEB SERVER (Per bypassare il limite Free di Render) ===
app_web = Flask('')

@app_web.route('/')
def home():
    return "Bot Re del giorno attivo!"

def run_web():
    app_web.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_web)
    t.daemon = True
    t.start()

# === CONFIGURAZIONE BOT ===
TOKEN = "8891286805:AAErmj2c6zs7YT1slmpj t6C2HNRfRopsiwU"
PAROLA_SEGRETA = "negrone"

re_di_oggi = None
data_ultimo_re = None

async def controlla_messaggio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global re_di_oggi, data_ultimo_re
    
    if not update.message or not update.message.text:
        return
        
    testo = update.message.text.lower().strip()
    oggi = date.today()
    
    if data_ultimo_re != oggi:
        re_di_oggi = None
        
    if PAROLA_SEGRETA in testo:
        utente = update.message.from_user
        nome_utente = f"@{utente.username}" if utente.username else utente.first_name
        
        if re_di_oggi is None:
            re_di_oggi = nome_utente
            data_ultimo_re = oggi
            await update.message.reply_text(
                f"👑 **ATTENZIONE TUTTI!** 👑\n\n"
                f"{nome_utente} ha scritto la parola magica ed è ufficialmente il **RE DEL GIORNO**! 👑✨"
            )
        elif re_di_oggi == nome_utente:
            await update.message.reply_text("👑 Sei già il Re di oggi, non ti allargare!")
        else:
            await update.message.reply_text(f"❌ Troppo tardi! Il Re di oggi è già {re_di_oggi}.")

if __name__ == '__main__':
    keep_alive()  # Avvia il serverino web
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), controlla_messaggio))
    print("Bot avviato e in ascolto...")
    app.run_polling()
