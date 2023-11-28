import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

import finpy_tse as fpy
import pandas as pd

from Functions import *

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global df
    df = pd.DataFrame()
    await update.message.reply_text("Wait to receive Data...")
    df, df_order_book = fpy.Get_MarketWatch()

    """Sends a message with three inline buttons attached."""
    keyboard = [
        [
            InlineKeyboardButton("1 تثبیت روند صعودی", callback_data="ascending1"),
            InlineKeyboardButton("چکش", callback_data="hammer"),
        ],
        [InlineKeyboardButton("روند صعودی 2", callback_data="ascending2")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Please choose:", reply_markup=reply_markup)



async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    query = update.callback_query
    
    dft = pd.DataFrame()

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()
    response = ''
    if query.data == "ascending1":
        dft = ascending1(df)
        for i in list(dft.index.values):
            response += '--\t'+str(i)+'\t-- \n'
        await query.edit_message_text('\n نتیجه فیلتر صعودی یک' + response)



    elif query.data == 'hammer':
        dft = hammer(df)
        for i in list(dft.index.values):
            response += '--\t'+str(i)+'\t-- \n'
        await query.edit_message_text('\n نتیجه فیلتر چکش'+ response)



    elif query.data == "ascending2":
        dft = ascending2(df)
        for i in list(dft.index.values):
            response += '--\t'+str(i)+'\t-- \n'
        await query.edit_message_text('\n نتیجه فیلتر صعودی دو' + response)



def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("6407366207:AAF_T6zZQPwKFMKhEr42tyZ4tnYYcsnoJgg").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
