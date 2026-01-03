import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import requests

token = '8518911704:AAGYQLajtsRaAF0hCo6GDz91rroY8lualAg'  # твой токен бота

bot = telebot.TeleBot(token)

# Клавиатура с кнопками
markup = ReplyKeyboardMarkup(resize_keyboard=True)
btn_almaty = KeyboardButton("Погода в Алматы")
btn_custom = KeyboardButton("Погода в другом городе")
markup.add(btn_almaty, btn_custom)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Привет, бро! Я бот с погодой. 😎\nНажми кнопку или напиши город.', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == "Погода в Алматы":
        get_weather(message, "Almaty")
    elif message.text == "Погода в другом городе":
        bot.reply_to(message, "Напиши название города (на английском или русском, например Москва или Almaty)")
    else:
        # Поддержка русских названий
        city_map = {
            "алматы": "Almaty",
            "астана": "Astana",
            "москва": "Moscow",
            "лондон": "London",
        }
        city = city_map.get(message.text.lower(), message.text)
        get_weather(message, city)

def get_weather(message, city):
    api_key = "ef6f07ece15f8270e83dd74185d56a16"  # твой ключ от OpenWeatherMap
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        desc = data['weather'][0]['description']
        bot.reply_to(message, f"Погода в {city}:\nТемпература: {temp}°C\n{desc.capitalize()}")
    else:
        bot.reply_to(message, "Город не найден или ключ ещё активируется. Подожди 30-60 мин и попробуй снова.")

print("Бот с погодой запущен...")
bot.infinity_polling()