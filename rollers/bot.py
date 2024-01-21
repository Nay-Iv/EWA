# bot.py

import logging
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

from rollers.main import parse_roll_input, EwaConfig

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def roll_handler(update, context: ContextTypes.DEFAULT_TYPE):
    roll_input = ''.join(context.args)

    roll_type, params = parse_roll_input(roll_input)
    roller = EwaConfig.roller

    if roll_type == 'rank':
        response = roller.roll_rank(params['rank']).pretty_result

    elif roll_type == 'chance':
        response = roller.roll_chance(params['bonus']).pretty_result

    elif roll_type == 'full':
        result = roller.roll_full(params['bonus'], params['rank'])
        response = '\t'.join([result['rank'].pretty_result, result['chance'].pretty_result])

    user = update.effective_user
    response_pretty = f"_{user.first_name}_ проходит проверку" + \
                      f"\tc результатом:\n *{response}*"

    await update.message.reply_text(text=response_pretty, parse_mode=ParseMode.MARKDOWN)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.application.add_handler(roll_handler)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="*ПОКАТАЕМ*", parse_mode=ParseMode.MARKDOWN)


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.application.remove_handler(roll_handler)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Ну и пожалуйста!")


async def help_handler(update, context: ContextTypes.DEFAULT_TYPE):
    help_text = "*/start* - запустить бота \n" +\
     "*/roll* - провести проверку \n" +\
     "Как провести проверку: +-n*R*, где +-n - бонус/штраф к Шансу, N - ранг атрибута\n" +\
     "Можно катать только Шанс: +-n \n" +\
     "Можно катать только Исход: *R*N \n" +\
     "*/stop* - заткнуть бота"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=help_text,  parse_mode=ParseMode.MARKDOWN)


if __name__ == '__main__':
    application = ApplicationBuilder().token(EwaConfig.tg_bot_token).build()

    start_handler = CommandHandler('start', start)
    roll_handler = CommandHandler('roll', roll_handler)
    help_handler = CommandHandler('help', help_handler)
    stop_handler = CommandHandler('stop', stop)

    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(stop_handler)

    application.run_polling()
