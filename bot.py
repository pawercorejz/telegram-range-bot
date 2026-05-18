import os
import tempfile
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

MAX_COUNT = 100_000


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 Я ГОТОВ — кидай диапазоны!\n\n"
        "Пример:\n"
        "74965360000-74965369999"
    )


async def handle_range(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().replace(" ", "")

    if "-" not in text:
        await update.message.reply_text(
            "❌ Формат:\n74965360000-74965369999"
        )
        return

    try:
        start_str, end_str = text.split("-", 1)

        start_num = int(start_str)
        end_num = int(end_str)

    except:
        await update.message.reply_text(
            "❌ Ошибка формата."
        )
        return

    if end_num <= start_num:
        await update.message.reply_text(
            "❌ Конец диапазона должен быть больше начала."
        )
        return

    count = end_num - start_num + 1

    if count > MAX_COUNT:
        await update.message.reply_text(
            f"❌ Слишком большой диапазон.\n"
            f"Максимум: {MAX_COUNT}"
        )
        return

    filename = f"{start_num}_{end_num}.csv"
    file_path = os.path.join(tempfile.gettempdir(), filename)

    # СУПЕР БЫСТРАЯ запись
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(
            "\n".join(
                str(number)
                for number in range(start_num, end_num + 1)
            )
        )

    # Отправка файла
    with open(file_path, "rb") as file:
        await update.message.reply_document(
            document=file,
            filename=filename,
            caption=f"✅ Готово\n📦 {count} номеров"
        )

    os.remove(file_path)


def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN не найден")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_range
        )
    )

    print("🚀 Бот запущен")

    app.run_polling()


if __name__ == "__main__":
    main()
    
