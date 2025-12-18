import telebot
from telebot import types

token = '7206783181:AAEJZVB9YZXWnNTHPwi9HY1MInv9wBEc82w'
bot = telebot.TeleBot(token)

def create_main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_help = types.KeyboardButton('/help')
    btn_cezar = types.KeyboardButton('/cezar')
    btn_start = types.KeyboardButton('/start')
    markup.add(btn_start, btn_help, btn_cezar)
    return markup

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = create_main_keyboard()
    bot.send_message(message.chat.id, "Привет! Я бот с кнопками. Выберите действие:", reply_markup=markup)

@bot.message_handler(commands=['help'])
def help(message):
    help_text = (
        "/start - старт работы с ботом\n"
        "/help - помощь\n"
        "/cezar - шифрование текста по шифру Цезаря\n\n"
        "Также вы можете использовать кнопки ниже для навигации!"
    )
    bot.send_message(message.chat.id, help_text, reply_markup=create_main_keyboard())

@bot.message_handler(commands=['cezar'])
def byCezar(message):
    bot.send_message(message.chat.id, "Введите текст для шифрования Цезаря:", reply_markup=create_main_keyboard())
    bot.register_next_step_handler(message, cezar_2)
def cezar(st):
    newSt = ""
    for i in st: 
        if i == "я":
            newSt += "а"
        elif i == "Я":
            newSt += "А"
        elif i == "Z":
            newSt += "A"
        elif i == "z":
            newSt += "a"
        else:
            newSt += chr(ord(i) + 1)
    return newSt

def cezar_2(message):
    result = cezar(message.text)
    bot.send_message(message.chat.id, f"Зашифрованный текст:\n{result}", reply_markup=create_main_keyboard())

@bot.message_handler(content_types=['photo'])
def photo(message):   
    fileID = message.photo[-1].file_id   
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("image.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.send_photo(message.chat.id, downloaded_file, reply_markup=create_main_keyboard())

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    if not message.text.startswith('/'):
        bot.send_message(message.chat.id, 
                        f"Вы написали: {message.text}\nИспользуйте кнопки или команды для работы с ботом.", 
                        reply_markup=create_main_keyboard())

if __name__ == '__main__':
    print("Бот запущен...")
    bot.infinity_polling()
