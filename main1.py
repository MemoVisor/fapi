import urllib

import requests
import telebot

token = "5126809018:AAE_NN_JWcn70WGPhSbKC142ajQbyM4lmzI"
bot = telebot.TeleBot(token)

URL = ''
MEME_NAME = "meme.jpg"


def validate_url(message):
    image_formats = ("image/png", "image/jpeg", "image/jpg")
    try:
        request_header = requests.head(message.text)
        is_image = request_header.headers["content-type"] in image_formats
        return is_image
    except:
        return False


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    fileID = message.photo[-1].file_id
    file = bot.get_file(fileID)
    url_photo = f"https://api.telegram.org/file/bot{token}/{file.file_path}"
    urllib.request.urlretrieve(url_photo, f"memes/{MEME_NAME}")
    bot.send_message(message.chat.id, url_photo)


@bot.message_handler(func=validate_url, content_types=['text'])
def handle_text(message):
    URL = message.text
    bot.reply_to(message, URL)


if __name__ == '__main__':
    bot.infinity_polling()

