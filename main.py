import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

# Токен берется из переменной окружения bothost (если не задан - ошибка)
TOKEN = os.getenv('BOT_TOKEN') or os.getenv('TELEGRAM_TOKEN')
if not TOKEN:
    raise ValueError("Токен не найден! Настройте его в bothost.")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_handler(message):
    markup = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton('🗣️ Получить консультацию', callback_data='consult')
    btn2 = InlineKeyboardButton('💡 Советы для покупок', callback_data='tips')
    btn3 = InlineKeyboardButton('❌ Самые частые ошибки продавцов', callback_data='errors')
    markup.add(btn1, btn2, btn3)
    
    text = (
        "Приветствую! 👋\n"
        "Ты попал в бота для получения поддержки по возврату денег, "
        "наложению санкций на мошенников и так далее! 🚀"
    )
    
    with open('start.png', 'rb') as photo:
        bot.send_photo(
            message.chat.id,
            photo,
            caption=text,
            reply_markup=markup,
            parse_mode='HTML'
        )

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == 'consult':
        bot.answer_callback_query(call.id, "Вы выбрали консультацию! Скоро ответим. 📞")
        bot.send_message(call.message.chat.id, "🔄 Запрос на консультацию отправлен. Ожидайте звонка!")
    elif call.data == 'tips':
        bot.answer_callback_query(call.id, "Полезные советы!")
        bot.send_message(call.message.chat.id, "💡 **Советы для безопасных покупок:**\n• Проверяйте отзывы продавца\n• Используйте защищенные платежи\n• Не переводите деньги заранее!")
    elif call.data == 'errors':
        bot.answer_callback_query(call.id, "Частые ошибки!")
        bot.send_message(call.message.chat.id, "❌ **Ошибки продавцов:**\n• Игнор жалоб покупателей\n• Отсутствие возврата\n• Фейковые товары")

if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling(none_stop=True)
