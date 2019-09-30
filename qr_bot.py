import telebot
from config import ACCESS_TOKEN
from telebot.types import Message
import requests
import json

bot = telebot.TeleBot(ACCESS_TOKEN)
chat_id = ''


@bot.message_handler(content_types=['photo'])
def check_image(message):
    if chat_id != '':
        #   декодируем qr-код
        file_id = message.photo[0].file_id
        file = bot.get_file(file_id)
        full_file_path = 'https://api.telegram.org/file/bot' + ACCESS_TOKEN + '/' + file.file_path
        image = requests.get(full_file_path)
        r = requests.post('http://api.foxtools.ru/v2/QR', files={'file': image.content})
        result = r.json()['response']['value']
        result = json.loads(result)
        #   отправляет результат на сервер склада

        r = requests.post('http://127.0.0.1/api/v1/items', data={
            "name": result['name'],
            "type": result['type'],
            "length": result['length'],
            "width": result['width'],
            "height": result['height']
        })
        print(r.text)
        # bot.send_message(chat_id, r.text)


@bot.message_handler(commands=['start'])
def set_chat_id(message: Message):
    global chat_id
    chat_id = message.chat.id
    bot.reply_to(message, "Hello!!!!")


bot.polling()