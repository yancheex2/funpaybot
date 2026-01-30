import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

# Токен берётся из переменных окружения (bothost / любой хостинг)
bot = telebot.TeleBot(os.getenv('BOT_TOKEN') or os.getenv('TELEGRAM_TOKEN'))

# ID админа (ТВОЙ Telegram ID). Узнать можно у @userinfobot
ADMIN_ID = 123456789  # ← ОБЯЗАТЕЛЬНО замени на свой ID

def send_with_logo(chat_id, text, reply_markup=None):
    """Отправка текста с картинкой start.png"""
    try:
        with open('start.png', 'rb') as photo:
            bot.send_photo(
                chat_id,
                photo,
                caption=text,
                reply_markup=reply_markup,
                parse_mode='HTML'
            )
    except FileNotFoundError:
        bot.send_message(chat_id, text, reply_markup=reply_markup, parse_mode='HTML')


# ---------- ГЛАВНОЕ МЕНЮ ----------

def main_menu_markup():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton('🗣️ Получить консультацию', callback_data='consult'),
        InlineKeyboardButton('💡 Советы для покупок', callback_data='tips'),
        InlineKeyboardButton('⚖️ Правила FunPay', callback_data='rules')
    )
    return markup

@bot.message_handler(commands=['start'])
def start_handler(message):
    text = (
        "🔥 <b>FunPay Support Bot</b> 🔥\n\n"
        "Привет! 👋\n"
        "Здесь ты можешь получить помощь по возврату денег, спорам с продавцами "
        "и безопасности покупок на FunPay.\n\n"
        "Выбери нужный раздел ниже 👇"
    )
    send_with_logo(message.chat.id, text, reply_markup=main_menu_markup())


# ---------- CALLBACK-КНОПКИ МЕНЮ ----------

@bot.callback_query_handler(func=lambda call: call.data == 'consult')
def cb_consult(call):
    bot.answer_callback_query(call.id)
    text = (
        "🗣️ <b>Получить консультацию</b>\n\n"
        "Опиши свою ситуацию одним сообщением:\n"
        "• Номер заказа на FunPay\n"
        "• Ник продавца\n"
        "• В чём проблема\n\n"
        "После этого я передам твоё обращение оператору. "
        "Ты можешь вести несколько диалогов, просто пиши из того же чата."
    )
    send_with_logo(call.message.chat.id, text)

@bot.callback_query_handler(func=lambda call: call.data == 'tips')
def cb_tips(call):
    bot.answer_callback_query(call.id)
    text = (
        "💡 <b>Советы для безопасных покупок на FunPay</b>\n\n"
        "✅ Проверяй рейтинг и количество отзывов продавца.\n"
        "✅ Внимательно читай описание товара и условия доставки.\n"
        "✅ Не подтверждай выполнение заказа, пока товар реально не получен.\n"
        "✅ Веди общение только в чате FunPay.\n\n"
        "🚫 <b>НЕЛЬЗЯ:</b>\n"
        "• Обмениваться контактами (Telegram, Discord и т.п.)\n"
        "• Получать/отправлять оплату вне FunPay\n"
        "• Вестись на слишком «выгодные» предложения."
    )
    send_with_logo(call.message.chat.id, text)

@bot.callback_query_handler(func=lambda call: call.data == 'rules')
def cb_rules(call):
    bot.answer_callback_query(call.id)
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton('📋 Общие правила', callback_data='rules1'),
        InlineKeyboardButton('🏪 Правила для продавцов', callback_data='rules2'),
        InlineKeyboardButton('⚖️ Ответственность продавцов', callback_data='rules3'),
        InlineKeyboardButton('🔙 Назад в меню', callback_data='back_to_menu')
    )
    text = (
        "⚖️ <b>Краткие правила FunPay</b>\n\n"
        "Выбери раздел, чтобы посмотреть основные пункты:\n"
        "• Общие правила общения и поведения\n"
        "• Что запрещено продавцам\n"
        "• В каких случаях продавец возвращает деньги"
    )
    send_with_logo(call.message.chat.id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'rules1')
def cb_rules1(call):
    bot.answer_callback_query(call.id)
    text = (
        "📋 <b>Общие правила FunPay (кратко)</b>\n\n"
        "1️⃣ Запрещён обмен любыми контактами (Telegram, Discord, ВК, телефон и т.д.).\n"
        "2️⃣ Нельзя заниматься спамом, флудом, накруткой отзывов, шантажом.\n"
        "3️⃣ Запрещены оскорбления, угрозы, политические и токсичные обсуждения.\n"
        "4️⃣ Нельзя раскрывать чужие личные данные и информацию о сделках.\n"
        "5️⃣ Мошенничество и обман ведут к полной блокировке и отказу в выплатах.\n\n"
        "Полный текст правил смотри на сайте FunPay."
    )
    send_with_logo(call.message.chat.id, text)

@bot.callback_query_handler(func=lambda call: call.data == 'rules2')
def cb_rules2(call):
    bot.answer_callback_query(call.id)
    text = (
        "🏪 <b>Правила для продавцов (кратко)</b>\n\n"
        "❌ Запрещено:\n"
        "• Передавать товар без оплаты через FunPay.\n"
        "• Просить подтвердить заказ до его фактического выполнения.\n"
        "• Игнорировать вопросы покупателей.\n"
        "• Выставлять фейковые предложения или неверные цены.\n"
        "• Продавать запрещённые категории (аккаунты со
