import telebot
import time
import random
import os
import requests
from config import TOKEN
from logic import gen_pass, gen_emodji, flip_coin,get_random_fact,count_down,get_help_text,get_random_number,get_ecology_organizations
import tf_keras as keras # Импортируем tf-keras - это совместимая версия Keras для работы с .h5 моделями
from tf_keras.models import load_model # Загружаем функцию load_model из tf_keras, чтобы открыть модель
from PIL import Image, ImageOps # Installing pillow instead of PIL
import numpy as np

bot = telebot.TeleBot(TOKEN)

def get_class(image_path, model_path="keras_model.h5", labels_path="labels.txt"):
    np.set_printoptions(suppress=True)
    model = load_model(model_path, compile=False)
    class_names = open(labels_path, "r").readlines()
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    image = Image.open(image_path).convert("RGB")
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    data[0] = normalized_image_array
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]
    return class_name[2:], confidence_score

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, f'Привет! Я бот {bot.get_me().first_name}!')

@bot.message_handler(content_types=['photo'])
def send_answer(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    file_name = file_info.file_path.split('/')[-1]
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.send_message(message.chat.id, 'Фото получено! Начинаем анализировать...')
    name, tochnost = get_class(file_name)
    bot.send_message(message.chat.id, f'На вышей фотографии - {name}  с вероятностью {tochnost}')
    
@bot.message_handler(commands=['heh'])
def send_heh(message):
    count_heh = int(message.text.split()[1]) if len(message.text.split()) > 1 else 5
    bot.reply_to(message, "he" * count_heh)

@bot.message_handler(commands=['bye'])
def send_bye(message):
    bot.reply_to(message, "Пока! Удачи!")

@bot.message_handler(commands=['password'])
def send_password(message):
    bot.send_message(message.chat.id, gen_pass(8))

@bot.message_handler(commands=['emodji'])
def send_emodji(message):
    bot.send_message(message.chat.id, gen_emodji())

@bot.message_handler(commands=['coin'])
def send_coin(message):
    bot.send_message(message.chat.id, flip_coin())

@bot.message_handler(commands=['fact'])
def send_fact(message):
    bot.send_message(message.chat.id, get_random_fact())

@bot.message_handler(commands=['countdown'])
def do_countdown(message):
    parts = message.text.split()
    if len(parts) < 2:
        bot.send_message(message.chat.id, "Укажите число после команды. Пример: /countdown 5")
        return

    try:
        number = int(parts[1])
        if number < 0:
            bot.send_message(message.chat.id, "Число должно быть неотрицательным.")
            return
        if number > 30:
            bot.send_message(message.chat.id, "Число не должно превышать 30.")
            return

        for i in range(number, -1, -1):
            bot.send_message(message.chat.id, str(i))
            time.sleep(1)

    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, укажите целое число. Пример: /countdown 10")

    number = int(parts[1])
    bot.send_message(message.chat.id, count_down(number))

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = get_help_text()
    bot.send_message(message.chat.id, help_text)

@bot.message_handler(commands=['mem'])
def send_mem(message):
    img_name = random.choice(os.listdir('Helper#1/images'))
    with open(f'Helper#1/images/{img_name}', 'rb') as f:  
            bot.send_photo(message.chat.id, f)  

def get_dog_image_url():    
        url = 'https://random.dog/woof.json'
        res = requests.get(url)
        data = res.json()
        return data['url']
    
    
@bot.message_handler(commands=['dog'])
def dog(message):
    '''По команде dog вызывает функцию get_dog_image_url и отправляет URL изображения утки'''
    image_url = get_dog_image_url()
    bot.reply_to(message, image_url)


@bot.message_handler(commands=['random'])
def send_random(message):
    parts = message.text.split()
    min_val = int(parts[1])
    max_val = int(parts[2])
    random_num = get_random_number(min_val, max_val)
    response = "Случайное число: " + random_num
    bot.send_message(message.chat.id, response)

@bot.message_handler(commands=['ecology'])
def send_random(message):
    ecology_text = get_ecology_organizations()
    bot.send_message(message.chat.id, ecology_text)

quiz_data = {}

quiz_data = {}

@bot.message_handler(commands=['quiz'])
def start_quiz(message):
    chat_id = message.chat.id
    quiz_data[chat_id] = {'step': 1, 'score': 0}
    bot.send_message(chat_id, "Вопрос 1:\nСколько времени разлагается пластиковая бутылка?")


@bot.message_handler(content_types=['text'])
def handle_answer(message):
    chat_id = message.chat.id
    
    if chat_id not in quiz_data:
        return 
    
    state = quiz_data[chat_id]
    user_answer = message.text.strip().lower()
    
    if state['step'] == 1:
        if user_answer in ["450 лет", "450", "около 450 лет"]:
            state['score'] += 1
            bot.send_message(chat_id, "✅ Правильно!")
        else:
            bot.send_message(chat_id, "❌ Неправильно. Верный ответ: 450 лет")
        state['step'] = 2
        bot.send_message(chat_id, "Вопрос 2:\nКак долго разлагается алюминиевая банка?")

    elif state['step'] == 2:
        if user_answer in ["80 лет", "80", "около 80 лет"]:
            state['score'] += 1
            bot.send_message(chat_id, "✅ Правильно!")
        else:
            bot.send_message(chat_id, "❌ Неправильно. Верный ответ: 80 лет")
        state['step'] = 3
        bot.send_message(chat_id, "Вопрос 3:\nСколько времени нужно, чтобы разложилась стеклянная бутылка?")

    elif state['step'] == 3:
        if user_answer in ["более 4000 лет", "4000+ лет", "больше 4000"]:
            state['score'] += 1
            bot.send_message(chat_id, "✅ Правильно!")
        else:
            bot.send_message(chat_id, "❌ Неправильно. Верный ответ: более 4000 лет")
        state['step'] = 4
        bot.send_message(chat_id, "Вопрос 4:\nКак быстро разлагается банановая кожура?")


    elif state['step'] == 4:
        if user_answer in ["1–2 недели", "1-2 недели", "1 2 недели", "за 1-2 недели"]:
            state['score'] += 1
            bot.send_message(chat_id, "✅ Правильно!")
        else:
            bot.send_message(chat_id, "❌ Неправильно. Верный ответ: 1–2 недели")
        state['step'] = 5
        bot.send_message(chat_id, "Вопрос 5:\nСколько лет разлагается полиэтиленовый пакет?")

    elif state['step'] == 5:
        if user_answer in ["100 лет", "100", "около 100 лет"]:
            state['score'] += 1
            bot.send_message(chat_id, "✅ Правильно!")
        else:
            bot.send_message(chat_id, "❌ Неправильно. Верный ответ: 100 лет")
        
        total = 5
        score = state['score']
        result = "Квиз завершён! Ваш результат: " + str(score) + "/" + str(total)
        bot.send_message(chat_id, result)
        
        del quiz_data[chat_id]

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.infinity_polling()
