import urllib

import requests
import telebot
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

app = FastAPI()


token = "5126809018:AAE_NN_JWcn70WGPhSbKC142ajQbyM4lmzI"
bot = telebot.TeleBot(token)

URL = ''
MEME_NAME = "meme.jpg"
MEME_PATH = f"memes/{MEME_NAME}"
MEME_DOC_NAME = "meme"
MEME_DOC_PATH = f"docs/{MEME_DOC_NAME}"


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


@bot.message_handler(content_types=['document'])
def handle_text_doc(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    ext = message.document.file_name.split('.')[-1]
    with open(f"{MEME_DOC_PATH}.{ext}", "wb") as new_file:
        new_file.write(downloaded_file)
    bot.reply_to(message, "Much nice")


@bot.message_handler(func=validate_url, content_types=['text'])
def handle_text(message):
    urllib.request.urlretrieve(message.text, MEME_PATH)
    bot.reply_to(message, "Much nice")


app.mount("/memes", StaticFiles(directory="memes"), name="memes")


@app.get("/")
async def root():
    return JSONResponse(content={"url": f"https://memovisor.saritasa.io/{MEME_PATH}"})

if __name__ == '__main__':
    bot.infinity_polling()

