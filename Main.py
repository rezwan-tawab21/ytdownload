import telebot
import yt_dlp
from telebot.types import ReplyKeyboardMarkup , InlineKeyboardButton , InlineKeyboardMarkup



api_key = ("7801225750:AAEqJnAvQgGI7pXXKemNkW3yp4qrdz1JOIU")
bot = telebot.TeleBot(api_key)

rep = ReplyKeyboardMarkup(resize_keyboard=True , one_time_keyboard=True)
rep.add("video" , "link")


user_url = {}


@bot.message_handler(commands=["start"])
def welcome(message):
    bot.reply_to(message, "Hello.Please enter youer youtube link")

#bot link save
@bot.message_handler(func=lambda message: message.text.startswith("http"))
def resive_link(message):
    user_url[message.chat.id] = message.text
    bot.send_message(message.chat.id , "Please select one of the options below" , reply_markup=rep)


#bot link or video
@bot.message_handler(func=lambda message: message.text in ["video" , "link"])
def download_youtube(message):

    url = user_url.get(message.chat.id)
    
    print("لینک دریافت شده:", url)
    if message.text == "video":
        video(message , url)
    elif message.text == "link":
        link(message , url)

#bot video download 
def video(message , url):
    try:
        ydl_opts = {}

        with yt_dlp.YoutubeDL(ydl_opts) as dlp:
            info = dlp.extract_info(url, download=True)
            video_url = dlp.prepare_filename(info)
            with open (video_url , "rb") as video:
                bot.send_video(message.chat.id , video)
    except Exception as e:
        bot.send_message(message.chat.id , f"erorr{e}")


#bot link download
def link(message , url):
    try:
        ydl_opts = {}
        with yt_dlp.YoutubeDL(ydl_opts) as dlp:
            info = dlp.extract_info(url, download=False)
            formats = info.get("formats")
            if formats:
                best = formats[-1]
                link = best.get("url")

            but = InlineKeyboardButton(text="download" , url=link)
            pp = InlineKeyboardMarkup(row_width=1)
            pp.add(but)
            
            bot.send_message(message.chat.id , "Video Link" , reply_markup=pp)
    except Exception as e:
        bot.send_message(message.chat.id , f"erorr\n{e}")        


bot.polling(skip_pending=True)



