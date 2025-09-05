import os
import time
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN", "8369016186:AAFgaMJ83GAT0gOTuouokT8ZKXDoR6i4rJA")
CANAL_TELEGRAM = "https://t.me/+lm9xHiJWrYhjOTUx"
GRUPO_DISCORD = "https://discord.gg/S3n3cuMP3J"
ADMIN_TAG = "@gh_wpr"
MIN_INTERVAL = 30
last_response_time = {}

RESPUESTAS = {
    "descargas": f"📥 Canal de descargas: {CANAL_TELEGRAM}",
    "descargar": f"📥 Canal de descargas: {CANAL_TELEGRAM}",
    "archivos": f"📥 Canal de descargas: {CANAL_TELEGRAM}",
    "gay": "🌈 El Shakala es gay. Confirmado por la comunidad.",
    "ts": f"🎧 Info de TeamSpeak: {CANAL_TELEGRAM}",
    "teamspeak": f"🎧 Info de TeamSpeak: {CANAL_TELEGRAM}",
    "discord": f"💬 Únete al Discord: {GRUPO_DISCORD}",
    "vpn": f"🔐 Info sobre VPN y ZeroTier: {CANAL_TELEGRAM}",
    "zero tier": f"🔐 Info sobre VPN y ZeroTier: {CANAL_TELEGRAM}",
    "zerotier": f"🔐 Info sobre VPN y ZeroTier: {CANAL_TELEGRAM}",
    "ayuda": f"🆘 {ADMIN_TAG}, alguien necesita ayuda.",
    "problemas": f"⚠️ {ADMIN_TAG}, hay un problema reportado.",
    "bateos": f"⚠️ {ADMIN_TAG}, hay un problema reportado.",
    "problema": f"⚠️ {ADMIN_TAG}, hay un problema reportado.",
    "error": f"⚠️ {ADMIN_TAG}, hay un problema reportado.",
    "errores": f"⚠️ {ADMIN_TAG}, hay un problema reportado.",
}

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    now = time.time()
    if user_id in last_response_time and now - last_response_time[user_id] < MIN_INTERVAL:
        return
    texto = update.message.text.lower()
    for palabra, respuesta in RESPUESTAS.items():
        if palabra in texto:
            await update.message.reply_text(respuesta)
            last_response_time[user_id] = now
            break

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), responder))
app.run_polling()
