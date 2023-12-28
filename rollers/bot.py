# bot.py

import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

from main import parse_roll_input, EwaConfig

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
        response = result['rank'].pretty_result+' '+result['chance'].pretty_result


    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


async def help_handler(update, context: ContextTypes.DEFAULT_TYPE):
    help_text = "Use /roll to roll dice!"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)

if __name__ == '__main__':
    application = ApplicationBuilder().token(EwaConfig.tg_bot_token).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    application.add_handler(CommandHandler('roll', roll_handler))
    application.add_handler(CommandHandler('help', help_handler))

    application.run_polling()
