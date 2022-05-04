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
username = ""
taglist = []
def readtag():
    global taglist
    if os.path.exists('SubscriptTag.txt'):
        with open('SubscriptTag.txt') as f:
            tags = f.readlines()
            for line in tags:
                user = line.split(' ')[0]
                tag = line.split(' ')[1]
                taglist.append(tag)
                # if user == username :
                #     taglist.append(tag)
    else :
        taglist = []
readtag()
##
load_dotenv()
token = os.getenv('TOKEN')
updater = Updater(token=token, use_context = True)
dispatcher = updater.dispatcher
##
def start(update, context): # 新增指令/start
    # update.message.reply_text('hello, {}'.format(update.message.from_user.first_name))
    message = update.message
    chat = message['chat']
    update.message.reply_text(text='HI  ' + str(chat['id']))
##
def downloader(update, context):
    DocName = str(update.message['chat']['id']) + ".txt"
    file = context.bot.get_file(update.message.document).download(custom_path = "DownloadFile/" + DocName)
    lines = ReadData(file)
    # writing to file
    try:
        with open("CustomFile/" + DocName, "w", encoding='utf-8') as WriteF:
            for line in lines :
                WriteF.write(line)
    except Exception as e:
        print(e)
        update.message.reply_text(text = "Sometihing get wrong")
    context.bot.send_document(chat_id = str(update.message['chat']['id']), document = open("CustomFile/" + DocName, 'rb'), filename = 'Convert.txt')
    # update.message.reply_text(text = "<a href='" + url + "'>" + info.get('title') + "</a>", parse_mode = ParseMode.HTML)

##
def ListCallback(update: Update, context: CallbackContext):
    update.callback_query.message.edit_text(text = update.callback_query.data)
##
dispatcher.add_handler(CommandHandler('start', start))
# dispatcher.add_handler(CallbackQueryHandler(ListCallback))
dispatcher.add_handler(MessageHandler(Filters.document, downloader))

updater.start_polling()
updater.idle()