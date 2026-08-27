import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

CS_URL = "https://t.me/GeneralPinjamTok_CS"


def main_menu():
    keyboard = [
        [
            InlineKeyboardButton("💰 Pembayaran", callback_data="payment"),
            InlineKeyboardButton("📋 Permohonan", callback_data="application"),
        ],
        [
            InlineKeyboardButton("🔎 Semak Status", callback_data="status"),
            InlineKeyboardButton("❓ FAQ", callback_data="faq"),
        ],
        [
            InlineKeyboardButton("🧑‍💼 Hubungi CS", url=CS_URL)
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "👋 *Selamat datang ke General PinjamTok!*\n\n"
        "🤖 Saya ialah bot bantuan automatik.\n\n"
        "Sila pilih menu di bawah:"
    )

    await update.message.reply_text(
        text,
        parse_mode="Markdown",
        reply_markup=main_menu()
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📚 *Bantuan General PinjamTok*\n\n"
        "/start - Buka menu utama\n"
        "/menu - Paparkan menu utama\n"
        "/help - Paparkan bantuan",
        parse_mode="Markdown",
        reply_markup=main_menu()
    )


async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)


async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()

    if query.data == "payment":

        text = (
            "💰 *PEMBAYARAN*\n\n"
            "Untuk pertanyaan berkaitan pembayaran, "
            "sila hubungi Customer Service untuk mendapatkan "
            "maklumat lanjut."
        )

    elif query.data == "application":

        text = (
            "📋 *PERMOHONAN*\n\n"
            "Untuk pertanyaan berkaitan permohonan, "
            "sila hubungi Customer Service untuk semakan lanjut."
        )

    elif query.data == "status":

        text = (
            "🔎 *SEMAK STATUS*\n\n"
            "Untuk semakan status, sila hubungi Customer Service "
            "dan sediakan maklumat rujukan yang berkaitan."
        )

    elif query.data == "faq":

        text = (
            "❓ *FAQ*\n\n"
            "• Bagaimana mendapatkan bantuan?\n"
            "Pilih menu *Hubungi CS*.\n\n"
            "• Bagaimana membuat semakan?\n"
            "Hubungi Customer Service untuk semakan.\n\n"
            "• Perlukan bantuan lanjut?\n"
            "Gunakan butang *Hubungi CS*."
        )

    elif query.data == "home":

        await query.edit_message_text(
            "🏠 *Menu Utama*\n\n"
            "Sila pilih pilihan anda:",
            parse_mode="Markdown",
            reply_markup=main_menu()
        )
        return

    keyboard = [
        [
            InlineKeyboardButton(
                "🔙 Kembali",
                callback_data="home"
            )
        ],
        [
            InlineKeyboardButton(
                "🧑‍💼 Hubungi CS",
                url=CS_URL
            )
        ]
    ]

    await query.edit_message_text(
        text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def message_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    text = update.message.text.lower().strip()

    if any(word in text for word in ["hai", "hello", "hi"]):

        await update.message.reply_text(
            "👋 Hai! Selamat datang ke *General PinjamTok*.\n\n"
            "Sila pilih menu di bawah:",
            parse_mode="Markdown",
            reply_markup=main_menu()
        )

    elif any(word in text for word in [
        "bayar",
        "pembayaran",
        "payment"
    ]):

        await update.message.reply_text(
            "💰 Untuk maklumat pembayaran, "
            "sila pilih menu *Pembayaran*.",
            parse_mode="Markdown",
            reply_markup=main_menu()
        )

    elif any(word in text for word in [
        "permohonan",
        "mohon"
    ]):

        await update.message.reply_text(
            "📋 Untuk maklumat permohonan, "
            "sila pilih menu *Permohonan*.",
            parse_mode="Markdown",
            reply_markup=main_menu()
        )

    elif any(word in text for word in [
        "status",
        "semak"
    ]):

        await update.message.reply_text(
            "🔎 Untuk semakan status, "
            "sila pilih menu *Semak Status*.",
            parse_mode="Markdown",
            reply_markup=main_menu()
        )

    else:

        await update.message.reply_text(
            "🤖 Maaf, saya tidak memahami mesej tersebut.\n\n"
            "Sila pilih menu di bawah atau hubungi Customer Service.",
            reply_markup=main_menu()
        )


def main():

    if not TOKEN:
        raise ValueError(
            "TELEGRAM_BOT_TOKEN belum ditetapkan."
        )

    app = Application.builder().token(TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("help", help_command)
    )

    app.add_handler(
        CommandHandler("menu", menu_command)
    )

    app.add_handler(
        CallbackQueryHandler(button_handler)
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            message_handler
        )
    )

    print("General PinjamTok Bot sedang berjalan...")

    app.run_polling()


if __name__ == "__main__":
    main()
