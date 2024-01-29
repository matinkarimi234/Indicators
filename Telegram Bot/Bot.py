import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

import finpy_tse as fpy
import pandas as pd
import jdatetime
from pathlib import Path

from Functions import *

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    await update.message.reply_text("Wait to receive Data...")

    """Sends a message with three inline buttons attached."""
    keyboard = [
        [
            InlineKeyboardButton("1 تثبیت روند صعودی", callback_data="ascending1")
        ],
        [
            InlineKeyboardButton("چکش", callback_data="hammer")
            
        ],
        [
            InlineKeyboardButton("روند صعودی 2", callback_data="ascending2")
        ],
        [
            InlineKeyboardButton("روند صعودی 1 و چکش", callback_data="hammer_ascend1")
        ],
        [
            InlineKeyboardButton("مقایسه سقف با سال 1399", callback_data="compare_99")
        ],

        [
            InlineKeyboardButton("روند صعودی 2 و چکش", callback_data="hammer_ascend2")
        ],
        [
            InlineKeyboardButton("مقایسه کف ماهانه و 99", callback_data="min_month_99")
        ],
        [
            InlineKeyboardButton("ایچیموکو کف و 99", callback_data="ichi_99")
        ],
        [
            InlineKeyboardButton("کف 3 ماهه و آستانه خرید", callback_data="Buy_Min")
        ],
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

    name_list_ichi = []
    if query.data == "ascending1":
        dft = ascending1()
        for i in dft['Ticker'].tolist():
            response += '--\t'+str(i)+'\t-- \n'
        await query.edit_message_text('\n نتیجه فیلتر صعودی یک' + response)



    elif query.data == 'hammer':
        dft = hammer()
        for i in dft['Ticker'].tolist():
            response += '--\t'+str(i)+'\t-- \n'
        await query.edit_message_text('\n نتیجه فیلتر چکش'+ response)



    elif query.data == "ascending2":
        dft = ascending2()
        for i in dft['Ticker'].tolist():
            response += '--\t'+str(i)+'\t-- \n'
        await query.edit_message_text('\n نتیجه فیلتر صعودی دو' + response)

        

    elif query.data == "hammer_ascend1":
        dft = hammer_ascend1()
        for i in dft['Ticker'].tolist():
            response += '--\t'+str(i)+'\t-- \n'
        await query.edit_message_text('\n نتیجه فیلتر صعودی 1 و چکش' + response)
    
    elif query.data == "hammer_ascend2":
        dft = hammer_ascend2()
        for i in dft['Ticker'].tolist():
            response += '--\t'+str(i)+'\t-- \n'
        await query.edit_message_text('\n نتیجه فیلتر صعودی 2 و چکش' + response)


    elif query.data == "compare_99":
        result = Compare_To_99()
        for i in list(result):
            response += '--\t'+str(i)+'\t-- \n'
        await query.edit_message_text('\n نتیجه فیلتر مقایسه سقف با 99' + response)


    elif query.data == "min_month_99":
        dft = Min_Month()
        for index,row in dft.iterrows():
            date = str(row['Date']).split('-')
            j_date = jdatetime.date.fromgregorian(day=int(date[2]),month=int(date[1]),year=int(date[0]))
            response += '--\t'+str(row['Ticker'])+'  '+str(j_date.strftime("%Y-%m-%d"))+'  \t-- \n'
            name_list_ichi.append(index)
        await query.edit_message_text('\n مقایسه کف ماهیانه و سقف 99' + response)

    elif query.data == "ichi_99":
        with open('names.txt','r',encoding='utf-8',errors = 'ignore') as f:
            name_list_ichi = f.readlines()
        print(name_list_ichi)
        photos = []
        count = 0
        num = str(len(name_list_ichi))
        for name in name_list_ichi:
            try:
                ticker, filename = name.split(',')
                Ichimoku(ticker.strip(),filename.strip())
            except Exception as e :
                print(e)
            finally:
                print(str(count)+'/'+num)
                count += 1

        data_folder = Path(r"/output/")
        for file in os.listdir('output'):
            photos.append(InputMediaPhoto(open(data_folder / file.strip()), 'rb'))
        
        await context.bot.send_media_group(chat_id=update.effective_chat.id, media=photos)
    elif query.data == "Buy_Min":
        dft = Min_Buy()
        for i in dft['Ticker'].tolist():
            response += '--\t'+str(i)+'\t-- \n'
        await query.edit_message_text('\n نتیجه کف 3 ماهه و فیلتر آستانه خرید' + response)


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
