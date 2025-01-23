import asyncio
from decouple import config
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from pytimeparse import parse

def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}".format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


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
    api_token = config('API_TOKEN')

    app = ApplicationBuilder().token(api_token).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))
    app.run_polling()


if __name__ == '__main__':
    main()
