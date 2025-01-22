import os
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from pytimeparse import parse

load_dotenv()
API_TOKEN = os.getenv('TG_TOKEN')

def render_progressbar(total, iteration, length=30, fill='█', empty_fill='░'):
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + empty_fill * (length - filled_length)
    percent = "{0:.1f}".format(100 * (iteration / float(total)))
    return '|{0}| {1:.1f}%'.format(bar, percent)

async def notify_progress(context: ContextTypes.DEFAULT_TYPE, chat_id: int, message_id: int, secs_left: int):
    total = secs_left
    for remaining in range(secs_left, -1, -1):
        progress_bar = render_progressbar(total, total - remaining)
        await context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=f"Осталось секунд: {remaining}\n{progress_bar}"
        )
        if remaining > 0:
            await asyncio.sleep(1)

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    delay = parse(user_input)

    message = await update.message.reply_text("Запускаю таймер...")
    await notify_progress(context, update.effective_chat.id, message.message_id, delay)
    await update.message.reply_text("Время вышло")

def main():
    app = ApplicationBuilder().token(API_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))
    app.run_polling()

if __name__ == '__main__':
    main()
