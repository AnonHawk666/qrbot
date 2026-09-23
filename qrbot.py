import io
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
import qrcode
from PIL import Image
from pyzbar.pyzbar import decode
import os
from dotenv import load_dotenv
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()

from telegram.request import HTTPXRequest

request = HTTPXRequest(
    connect_timeout=60,
    read_timeout=60,
    write_timeout=60,
    pool_timeout=60
)

app = (
    ApplicationBuilder()
    .token(BOT_TOKEN)
    .request(request)
    .build()
)




# ---------- START ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "👋 *Welcome to QR Bot*\n\n"
        "*Private Chat:*\n"
        "• Send any text → QR generated\n"
        "• Send QR image → Decoded\n\n"
        "*Groups:*\n"
        "• /qr <text> → Generate QR\n"
        "• Send QR image with caption `/decode` → Decode\n"
    )
    await update.message.reply_text(text, parse_mode="Markdown")


# ---------- QR GENERATOR ----------
def generate_qr(text: str) -> io.BytesIO:
    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(text)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    bio = io.BytesIO()
    bio.name = "qr.png"
    img.save(bio, "PNG")
    bio.seek(0)
    return bio


# ---------- /qr ----------
async def qr_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type == "private":
        await update.message.reply_text(
            "❌ /qr works only in groups.\n"
            "Just send text directly in private chat."
        )
        return

    if not context.args:
        await update.message.reply_text("❌ Usage: /qr <text>")
        return

    text = " ".join(context.args)
    qr_img = generate_qr(text)

    await update.message.reply_photo(
        photo=qr_img,
        caption=f'📦 QR Generated for text "{text}"'
    )


# ---------- BLOCK /decode IN PRIVATE ----------
async def decode_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type == "private":
        await update.message.reply_text(
            "❌ /decode works only in groups.\n"
            "Just send the QR image directly in private chat."
        )


# ---------- PRIVATE TEXT → QR ----------
async def text_to_qr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type != "private":
        return

    text = update.message.text
    qr_img = generate_qr(text)

    await update.message.reply_photo(
        photo=qr_img,
        caption=f'📦 QR Generated for text "{text}"'
    )


# ---------- DECODE QR IMAGE ----------
async def decode_qr(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # In group → caption must be /decode
    if update.message.chat.type != "private":
        if update.message.caption != "/decode":
            return

    photo = update.message.photo[-1]
    file = await photo.get_file()

    bio = io.BytesIO()
    await file.download_to_memory(bio)
    bio.seek(0)

    img = Image.open(bio)
    decoded = decode(img)

    if not decoded:
        await update.message.reply_text("❌ No QR code found")
        return

    result = decoded[0].data.decode("utf-8")
    await update.message.reply_text(
        f"🔓 *Decoded QR:*\n\n`{result}`",
        parse_mode="Markdown"
    )


# ---------- MAIN ----------
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("qr", qr_command))
    app.add_handler(CommandHandler("decode", decode_command))

    # Text → QR (PRIVATE ONLY, COMMANDS IGNORED)
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            text_to_qr
        )
    )

    # Photo → Decode
    app.add_handler(MessageHandler(filters.PHOTO, decode_qr))

    print("✅ QR Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
