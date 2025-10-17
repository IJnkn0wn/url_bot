import telebot
import json
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загрузка токена
try:
    with open('telegram_token.json', 'r') as f:
        token_data = json.load(f)
        BOT_TOKEN = token_data.get('token') or token_data.get('bot_token') or list(token_data.values())[0]
    logger.info("Токен загружен из файла")
except Exception as e:
    logger.error(f"Ошибка загрузки токена: {e}")
    # Вставьте ваш токен здесь
    BOT_TOKEN = "ВАШ_ТОКЕН_ЗДЕСЬ"

bot = telebot.TeleBot(BOT_TOKEN)

# URL вашего GitHub Pages
WEB_APP_URL = "https://ВАШ_USERNAME.github.io/ВАШ_РЕПОЗИТОРИЙ/webapp.html"

@bot.message_handler(commands=['start', 'help'])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(
        text="📊 Открыть Яндекс Таблицы", 
        web_app=telebot.types.WebAppInfo(url=WEB_APP_URL)
    ))
    
    bot.send_message(
        message.chat.id,
        "🤖 **Бот для работы с Яндекс Таблицами**\n\n"
        "Нажмите кнопку ниже чтобы открыть удобный интерфейс "
        "для заполнения ваших таблиц!\n\n"
        "✨ **Как использовать:**\n"
        "1. Откройте интерфейс\n"
        "2. Вставьте ссылку на Яндекс Таблицу\n"
        "3. Заполните форму\n"
        "4. Данные автоматически сохранятся",
        parse_mode='Markdown',
        reply_markup=markup
    )

@bot.message_handler(content_types=['web_app_data'])
def handle_web_app_data(message):
    try:
        data = json.loads(message.web_app_data.data)
        logger.info(f"Получены данные: {data}")
        
        response_text = f"""
✅ **Данные успешно получены!**

📋 **Лист:** `{data['sheet']}`
👤 **ФИО:** {data['fio']}
📅 **Дата:** {data['date']}
⏰ **Время:** {data['time']}
🎯 **Тема:** {data['topic']}
📊 **Статус:** {data['status']}
📝 **Примечание:** {data['note']}

Скопируйте эти данные в вашу Яндекс Таблицу.
"""
        
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(
            "📊 Добавить еще данные", 
            web_app=telebot.types.WebAppInfo(url=WEB_APP_URL)
        ))
        
        bot.send_message(
            message.chat.id,
            response_text,
            parse_mode='Markdown',
            reply_markup=markup
        )
        
    except Exception as e:
        logger.error(f"Ошибка обработки данных: {e}")
        bot.send_message(message.chat.id, "❌ Произошла ошибка при обработке данных")

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    if message.text.lower() in ["таблицы", "форма", "заполнить", "webapp"]:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(
            "📊 Открыть интерфейс", 
            web_app=telebot.types.WebAppInfo(url=WEB_APP_URL)
        ))
        bot.send_message(message.chat.id, "Нажмите кнопку чтобы открыть интерфейс:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Используйте /start для начала работы")

if __name__ == "__main__":
    logger.info("🤖 Бот запускается...")
    logger.info(f"🌐 Web App URL: {WEB_APP_URL}")
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logger.error(f"Ошибка бота: {e}")
