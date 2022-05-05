from telegram.ext import Updater # 更新者
from telegram.ext import CommandHandler, CallbackQueryHandler # 註冊處理 一般用 回答用
from telegram.ext import MessageHandler, Filters # Filters過濾訊息
from telegram.ext import CallbackContext
from telegram import InlineKeyboardMarkup, InlineKeyboardButton # 互動式按鈕
from telegram import ParseMode, Update
from dotenv import load_dotenv
from ReadEvent import *
import os
##
load_dotenv()
token = os.getenv('TOKEN')
updater = Updater(token=token, use_context = True)
dispatcher = updater.dispatcher
##
def start(update, context): # 新增指令/start
    message = update.message
    chat = message['chat']
    update.message.reply_text(text='HI  ' + str(chat['username']) + '. Enter /help to get more information.')
##
def help(update, context): # 新增指令/help
    message = update.message
    chat = message['chat']
    update.message.reply_text(text='This Bot is use to convert the txt file that didn\'t match the encode setting of your computer.\nJust send the txt file you want to decode.\n Then we will send the converted file with utf-8 encoded txt file.')
##
def downloader(update, context):
    DocName = str(update.message['chat']['id']) + '.txt'
    file = context.bot.get_file(update.message.document).download(custom_path = 'DownloadFile/' + DocName)
    TxtDetail = ReadData(file)
    lines = TxtDetail['data']
    update.message.reply_text(text = 'encoding:' + TxtDetail['encoding'] + '\n' + 'confidence:' + str(TxtDetail['confidence']) + '\n' + 'language:' + TxtDetail['language'])
    # writing to file
    try:
        with open('CustomFile/' + DocName, 'w', encoding='utf-8') as WriteF:
            for line in lines :
                WriteF.write(line)
    except Exception as e:
        print(e)
        update.message.reply_text(text = 'Sometihing get wrong')
    context.bot.send_document(chat_id = str(update.message['chat']['id']), document = open('CustomFile/' + DocName, 'rb'), filename = 'Convert.txt')
    # update.message.reply_text(text = "<a href='" + url + "'>" + info.get('title') + "</a>", parse_mode = ParseMode.HTML)

##
# def ListCallback(update: Update, context: CallbackContext):
#     update.callback_query.message.edit_text(text = update.callback_query.data)
##
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', help))
# dispatcher.add_handler(CallbackQueryHandler(ListCallback))
dispatcher.add_handler(MessageHandler(Filters.document, downloader))

updater.start_polling()
updater.idle()