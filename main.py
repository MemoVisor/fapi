import telebot
from fastapi import FastAPI

app = FastAPI()


bot = telebot.TeleBot("5126809018:AAE_NN_JWcn70WGPhSbKC142ajQbyM4lmzI")

URL = ''


def validate_url(message):
    return True


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    print(f'message.photo = {message.photo}')
    fileID = message.photo[-1].file_id
    print(f'fileID = {fileID}')
    file = bot.get_file(fileID)
    print(f'file.file_path = {file.file_path}')

    bot.send_message(message.chat.id, message)


@bot.message_handler(func=validate_url, content_types=['text'])
def handle_text(message):
    URL = message.text
    bot.reply_to(message, URL)


@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == '__main__':
    bot.infinity_polling()

