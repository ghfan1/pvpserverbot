import os
import time
import logging
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# ========================
# Configuración de logs
# ========================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ========================
# Token del bot
# ========================
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("❌ Falta la variable de entorno BOT_TOKEN")

# ========================
# Enlaces y tags
# ========================
CANAL_TELEGRAM = "https://t.me/+lm9xHiJWrYhjOTUx"
GRUPO_DISCORD = "https://discord.gg/S3n3cuMP3J"
ADMIN_TAG = "@gh_wpr"

# ========================
# Control de spam
# ========================
MIN_INTERVAL = 30  # tiempo mínimo entre respuestas por usuario (segundos)
last_response_time = {}

# ========================
# Diccionario de respuestas
# ========================
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
# Función de respuesta
# ========================
async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    user_id = update.message.from_user.id
    now = time.time()

    # Control de spam por usuario
    if user_id in last_response_time and now - last_response_time[user_id] < MIN_INTERVAL:
        return

    texto = update.message.text.lower()
    for palabra, respuesta in RESPUESTAS.items():
        if palabra in texto:
            await update.message.reply_text(respuesta)
            last_response_time[user_id] = now
            break

# ========================
# Servidor Flask (Render necesita puerto abierto)
# ========================
app_flask = Flask(__name__)

@app_flask.route("/")
def index():
    return "🤖 Bot de Telegram activo", 200

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app_flask.run(host="0.0.0.0", port=port)

# ========================
# Inicialización del bot
# ========================
def main():
    # Levantar Flask en un hilo aparte
    threading.Thread(target=run_flask, daemon=True).start()

    # Levantar bot en modo polling
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), responder))
    logging.info("🤖 Bot iniciado y escuchando mensajes...")
    app.run_polling()

if __name__ == "__main__":
    main()
