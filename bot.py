import os
import csv
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters


TOKEN = os.getenv("BOT_TOKEN")

pattern = re.compile(r"(\d+)-(\d+)")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    match = pattern.match(text)

    if not match:
        await update.message.reply_text("Формат: 1000-2000")
        return

    start = int(match.group(1))
    end = int(match.group(2))

    if start > end:
        await update.message.reply_text("Ошибка: начало больше конца")
        return

    filename = f"{start}_{end}.csv"

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        for num in range(start, end + 1):
            writer.writerow([num])

    with open(filename, "rb") as f:
        await update.message.reply_document(f)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
