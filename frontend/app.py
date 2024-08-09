from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import Application, CommandHandler, CallbackContext, CallbackQueryHandler, ContextTypes, MessageHandler, ConversationHandler, filters
# import re
import logging
import os
from dotenv import load_dotenv

logging.basicConfig(
    format = '%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s',
    level = logging.INFO
)

logger = logging.getLogger(__name__)

load_dotenv("../.env")
TOKEN = os.getenv("token")

# define states
SCAM_OR_NOT, AI_ANALYSE = range(2)


async def start(update: Update, context: CallbackContext):
    reply_keyboard = [
        ["🙅🏻 No, I have not been scammed"],
        ["👮🏻‍♂️ Yes, but I have NOT made a police report"],
        ["🧑🏻‍⚖️ Yes, and I have made a police report"]
    ]

    await update.message.reply_text(
        "Oh no! We are a small claims bot, here to determine if you are able to sue your scammer privately.\n\nIf you are here, can I assume you have been scammed?",
        # reply_markup=InlineKeyboardMarkup(keyboard),
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard = True)
    )

    return SCAM_OR_NOT

async def not_scammed(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "That's good to hear! If you need me, I'll be here anytime!\n\n"
        "Use /start if you would like help with small claims, or use /about to find out more about what I can do.",
        reply_markup = ReplyKeyboardRemove())
    return ConversationHandler.END

async def no_police_report(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "It's best to file a police report first!\n\n"
        "Go to National Crime Prevention Council's <a href = 'scamalert.sg/resources/gotscammed'>Scam Alert page</a> for what information to include in the Police report"
        "You can then file a report <a href = 'https://eservices1.police.gov.sg/phub/eservices/landingpage/police-report'>online</a> or at your nearest <a href = 'https://www.police.gov.sg/Contact-Us'>Neighbourhood Police Center</a>\n\n"
        "Once you have made a police report, you can consider if you want to take private legal action as well. If you need me then, I'll be here!\n\n"
        "Use /start again if you would like help with small claims, or use /about to find out more about what I can do.",
        # reply_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard = True),
        reply_markup = ReplyKeyboardRemove(),
        parse_mode = "HTML"
        )
    return ConversationHandler.END

async def yes_police_report(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Good to hear that. "
        "Small Claims can be used to ... placeholder placeholder something "
        "Tell me more."
    )
    return AI_ANALYSE

async def analyse(update: Update, context: CallbackContext):
    # do ai stuff here

    raise Exception(update.message.text)
    await update.message.reply_text("Alright, I get it! Or I would have if the AI worked")


async def quit(update: Update, context: CallbackContext):
    await update.message.reply_text("Thats alright!\n\n"
                                    "Use /start again if you would like help with small claims, or use /about to find out more about what I can do.")
    return ConversationHandler.END

def main():
    app = Application.builder().token(TOKEN).build()

    # slash commands
    # app.add_handler(CommandHandler("start", start))
    # app.add_handler(CommandHandler("hint", hint))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)], # enter with start
        states={
            SCAM_OR_NOT: [
                MessageHandler(filters.Regex("^🙅🏻 No, I have not been scammed$"), not_scammed),
                MessageHandler(filters.Regex("^👮🏻‍♂️ Yes, but I have NOT made a police report$"), no_police_report),
                MessageHandler(filters.Regex("^🧑🏻‍⚖️ Yes, and I have made a police report$"), yes_police_report),
            ],
            AI_ANALYSE: [
                MessageHandler(
                    filters.TEXT, analyse
                )
            ],
        },
        fallbacks=[CommandHandler("quit", quit)],
    )

    app.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()