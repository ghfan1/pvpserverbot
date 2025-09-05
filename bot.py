import os
import time
import logging
from flask import Flask
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

# ========================
# Configuración
# ========================
TOKEN = os.getenv("BOT_TOKEN")

CANAL_TELEGRAM = "https://t.me/+lm9xHiJWrYhjOTUx"
GRUPO_DISCORD = "https://discord.gg/S3n3cuMP3J"
ADMIN_TAG = "@gh_wpr"

MIN_INTERVAL = 30  # Anti-spam por usuario
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

# ========================
# Logging
# ========================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# ========================
# Flask (opcional, keep-alive)
# ========================
server = Flask(__name__)

@server.route("/")
def home():
    return "🤖 Bot corriendo en grupo 🚀"

# ========================
# Función de respuesta en grupo
# ========================
async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    user_id = update.message.from_user.id
    now = time.time()

    # Anti-spam por usuario
    if user_id in last_response_time and now - last_response_time[user_id] < MIN_INTERVAL:
        return

    texto = update.message.text.lower()
    for palabra, respuesta in RESPUESTAS.items():
        if palabra in texto:
            # Responde en el mismo grupo
            await context.bot.send_message(chat_id=update.message.chat.id, text=respuesta)
            last_response_time[user_id] = now
            break

# ========================
# Main
# ========================
def main():
    if not TOKEN:
        raise ValueError("❌ BOT_TOKEN no encontrado")

    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

    print("🤖 Bot iniciado en grupo...")
    application.run_polling()

if __name__ == "__main__":
    main()
