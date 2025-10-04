token = '7206783181:AAEJZVB9YZXWnNTHPwi9HY1MInv9wBEc82w'
import telebot

bot = telebot.TeleBot(token)

#@bot.message_handler(content_types=["text"])
#def repeat_all_messages(message): # Название функции не играет никакой роли
    #bot.send_message(message.chat.id, cezar(message.text))
@bot.message_handler(content_types=['photo'])
def photo(message):   
     fileID = message.photo[-1].file_id   
     file_info = bot.get_file(fileID)
     downloaded_file = bot.download_file(file_info.file_path)
     with open("image.jpg", 'wb') as new_file:
         new_file.write(downloaded_file)
     bot.send_photo(message.chat.id, downloaded_file)
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,"Привет!")
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "/start - старт работы с ботом\n/help - помощь\n/cezar - шифрование текста по шифру Цезаря\n")
@bot.message_handler(commands=['cezar'])
def byCezar(message):
    bot.send_message(message.chat.id, "Введите текст...")
    bot.register_next_step_handler(message, cezar_2)
def cezar_2(message):
    bot.send_message(message.chat.id, cezar(message.text))
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
            newSt += "а"
        else:
            newSt += chr(ord(i) + 1)
    return newSt
if __name__ == '__main__':
     bot.infinity_polling()
