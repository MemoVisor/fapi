import urllib

import requests
import telebot
from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()


token = "5126809018:AAE_NN_JWcn70WGPhSbKC142ajQbyM4lmzI"
bot = telebot.TeleBot(token)

URL = ''
MEME_NAME = "meme.jpg"
MEME_PATH = f"memes/{MEME_NAME}"


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
    urllib.request.urlretrieve(url_photo, MEME_PATH)
    bot.reply_to(message, "Much nice")


@bot.message_handler(func=validate_url, content_types=['text'])
def handle_text(message):
    urllib.request.urlretrieve(message.text, MEME_PATH)
    bot.reply_to(message, "Much nice")


@app.get("/")
async def root():
    return FileResponse(MEME_PATH)

if __name__ == '__main__':
    bot.infinity_polling()

