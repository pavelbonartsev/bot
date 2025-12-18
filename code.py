import telebot
from telebot import types
import json
import os

token = '7206783181:AAEJZVB9YZXWnNTHPwi9HY1MInv9wBEc82w'
bot = telebot.TeleBot(token)

HISTORY_FILE = 'cezar_history.json'

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_history(history):
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def get_user_history(user_id):
    history = load_history()
    return history.get(str(user_id), {'encrypted': [], 'decrypted': []})

def add_to_history(user_id, original_text, processed_text, is_encryption=True):
    history = load_history()
    user_id_str = str(user_id)
    
    if user_id_str not in history:
        history[user_id_str] = {'encrypted': [], 'decrypted': []}
    
    if is_encryption:
        history[user_id_str]['encrypted'].append({
            'original': original_text,
            'encrypted': processed_text
        })
        if len(history[user_id_str]['encrypted']) > 50:
            history[user_id_str]['encrypted'] = history[user_id_str]['encrypted'][-50:]
    else:
        history[user_id_str]['decrypted'].append({
            'original': original_text,
            'decrypted': processed_text
        })
        if len(history[user_id_str]['decrypted']) > 50:
            history[user_id_str]['decrypted'] = history[user_id_str]['decrypted'][-50:]
    
    save_history(history)

def create_main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_help = types.KeyboardButton('/help')
    btn_cezar = types.KeyboardButton('/cezar')
    btn_start = types.KeyboardButton('/start')
    btn_history = types.KeyboardButton('/history')
    markup.add(btn_start, btn_help, btn_cezar, btn_history)
    return markup

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = create_main_keyboard()
    welcome_text = "Привет! Я бот с кнопками. Выберите действие:\n\n• /cezar - шифрование текста\n• /history - посмотреть историю\n• /help - справка"
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

@bot.message_handler(commands=['help'])
def help(message):
    help_text = "Доступные команды:\n/start - старт работы\n/help - помощь\n/cezar - шифрование текста\n/history - история шифрований\n\nБот запоминает все тексты!"
    bot.send_message(message.chat.id, help_text, reply_markup=create_main_keyboard())

@bot.message_handler(commands=['history'])
def show_history(message):
    user_history = get_user_history(message.from_user.id)
    
    if not user_history['encrypted'] and not user_history['decrypted']:
        bot.send_message(message.chat.id, "Ваша история пуста.", reply_markup=create_main_keyboard())
        return
    
    response = "📜 История шифрований:\n\n"
    
    if user_history['encrypted']:
        response += "🔒 Зашифрованные тексты:\n"
        for i, item in enumerate(user_history['encrypted'][-10:], 1):
            response += f"{i}. Оригинал: {item['original'][:30]}... → {item['encrypted'][:30]}...\n"
    
    if user_history['decrypted']:
        response += "\n🔓 Расшифрованные тексты:\n"
        for i, item in enumerate(user_history['decrypted'][-10:], 1):
            response += f"{i}. Зашифровано: {item['original'][:30]}... → {item['decrypted'][:30]}...\n"
    
    response += "\nИспользуйте /cezar для нового шифрования."
    bot.send_message(message.chat.id, response, reply_markup=create_main_keyboard())

@bot.message_handler(commands=['cezar'])
def byCezar(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_encrypt = types.KeyboardButton('🔒 Зашифровать')
    btn_decrypt = types.KeyboardButton('🔓 Расшифровать')
    btn_back = types.KeyboardButton('Назад')
    markup.add(btn_encrypt, btn_decrypt, btn_back)
    
    bot.send_message(message.chat.id, 
                     "Выберите действие:\n• '🔒 Зашифровать' - зашифровать текст\n• '🔓 Расшифровать' - расшифровать текст\n• 'Назад' - вернуться в меню", 
                     reply_markup=markup)
    bot.register_next_step_handler(message, choose_cezar_action)

def choose_cezar_action(message):
    if message.text == '🔒 Зашифровать':
        bot.send_message(message.chat.id, "Введите текст для шифрования:", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, lambda m: process_cezar(m, encrypt=True))
    elif message.text == '🔓 Расшифровать':
        bot.send_message(message.chat.id, "Введите текст для расшифровки:", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, lambda m: process_cezar(m, encrypt=False))
    elif message.text == 'Назад':
        bot.send_message(message.chat.id, "Возврат в главное меню.", reply_markup=create_main_keyboard())
    else:
        bot.send_message(message.chat.id, "Используйте кнопки для выбора действия.", reply_markup=create_main_keyboard())

def cezar_encrypt(st):
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

def cezar_decrypt(st):
    newSt = ""
    for i in st: 
        if i == "а":
            newSt += "я"
        elif i == "А":
            newSt += "Я"
        elif i == "A":
            newSt += "Z"
        elif i == "a":
            newSt += "z"
        else:
            newSt += chr(ord(i) - 1)
    return newSt

def process_cezar(message, encrypt=True):
    user_text = message.text
    
    if encrypt:
        result = cezar_encrypt(user_text)
        action = "зашифрован"
        add_to_history(message.from_user.id, user_text, result, is_encryption=True)
    else:
        result = cezar_decrypt(user_text)
        action = "расшифрован"
        add_to_history(message.from_user.id, user_text, result, is_encryption=False)
    
    response = f"✅ Текст {action}!\n\n📝 Оригинал: {user_text}\n🔐 Результат: {result}\n\nЗапись сохранена в истории (/history)"
    bot.send_message(message.chat.id, response, reply_markup=create_main_keyboard())

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
        if message.text not in ['🔒 Зашифровать', '🔓 Расшифровать', 'Назад']:
            bot.send_message(message.chat.id, 
                            f"Вы написали: {message.text}\nИспользуйте кнопки или команды для работы с ботом.", 
                            reply_markup=create_main_keyboard())

if __name__ == '__main__':
    print("Бот запущен...")
    bot.infinity_polling()
