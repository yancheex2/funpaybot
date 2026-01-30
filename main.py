import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

# Токен полностью удалён - bothost подставит автоматически
bot = telebot.TeleBot(os.getenv('BOT_TOKEN') or os.getenv('TELEGRAM_TOKEN'))

ADMIN_ID = 5841365763  # ← ЗАМЕНИТЕ НА ВАШ Telegram ID (узнайте @userinfobot)

def send_with_logo(chat_id, text):
    """Отправка с логотипом"""
    try:
        with open('start.png', 'rb') as photo:
            bot.send_photo(chat_id, photo, caption=text, parse_mode='HTML')
    except:
        bot.send_message(chat_id, text, parse_mode='HTML')

@bot.message_handler(commands=['start'])
def start_handler(message):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton('🗣️ Консультация', callback_data='consult'),
        InlineKeyboardButton('💡 Советы', callback_data='tips'),
        InlineKeyboardButton('⚖️ Правила', callback_data='rules')
    )
    text = "🔥 <b>FunPay Support Bot</b> 🔥\n\nПривет! Помощь по возвратам и спорам на FunPay!"
    send_with_logo(message.chat.id, text)

@bot.message_handler(func=lambda message: True)
def handle_consultation(message):
    """Все сообщения после /start = консультация"""
    if message.text.startswith('/'):
        return
        
    # ✅ РЕАЛ-ТАЙМ: сразу отправляем ВАМ сообщение + ID клиента
    client_name = message.from_user.first_name or "Клиент"
    forward_text = (
        f"👤 <b>Новая консультация #{message.chat.id}</b>\n"
        f"Имя: {client_name} (@{message.from_user.username or 'нет'})\n"
        f"⏰ {message.date}\n\n"
        f"💬 <b>Сообщение:</b>\n{message.text}\n\n"
        f"📱 Ответить: /reply_{message.chat.id} текст"
    )
    
    # Отправляем админу с кнопками быстрого ответа
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('✅ Закрыто', callback_data=f'close_{message.chat.id}'))
    markup.add(InlineKeyboardButton('💰 Возврат 100%', callback_data=f'refund_{message.chat.id}'))
    markup.add(InlineKeyboardButton('⚠️ Жалоба', callback_data=f'claim_{message.chat.id}'))
    
    bot.send_photo(
        ADMIN_ID, 
        open('start.png', 'rb'), 
        caption=forward_text,
        reply_markup=markup,
        parse_mode='HTML'
    )
    
    # Подтверждение клиенту
    send_with_logo(message.chat.id, 
        f"✅ Ваше сообщение получено!\n"
        f"🕐 Ожидайте ответа в течение 10 минут\n"
        f"ID консультации: <code>{message.chat.id}</code>")

# Быстрые ответы админа
@bot.message_handler(func=lambda m: m.text.startswith('/reply_'))
def admin_reply(message):
    if message.from_user.id != ADMIN_ID:
        return
        
    parts = message.text.split('_', 2)
    if len(parts) < 3:
        return
        
    client_id = int(parts[1])
    reply_text = parts[2]
    
    bot.send_message(client_id, f"👨‍💼 <b>Ответ поддержки:</b>\n\n{reply_text}", parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: call.data.startswith(('close_', 'refund_', 'claim_')))
def admin_actions(call):
    if call.from_user.id != ADMIN_ID:
        return
        
    action, client_id = call.data.split('_', 1)
    client_id = int(client_id)
    
    if action == 'close':
        bot.send_message(client_id, "✅ <b>Консультация закрыта!</b>\nСпасибо за обращение!", parse_mode='HTML')
    elif action == 'refund':
        bot.send_message(client_id, "💰 <b>Возврат одобрен 100%!</b>\nИнструкция: funpay.com/support", parse_mode='HTML')
    elif action == 'claim':
        bot.send_message(client_id, "⚠️ <b>Жалоба принята</b>\n📝 Подробности в личном кабинете FunPay", parse_mode='HTML')
    
    bot.answer_callback_query(call.id, "Отправлено клиенту!")
    bot.edit_message_caption(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        caption=call.message.caption + f"\n\n✅ <b>Действие выполнено</b>",
        parse_mode='HTML'
    )

# Остальные колбэки (советы, правила) - как раньше
@bot.callback_query_handler(func=lambda call: call.data in ['tips', 'rules', 'rules1', 'rules2', 'rules3'])
def other_callbacks(call):
    bot.answer_callback_query(call.id)
    # ... (код советов и правил из предыдущей версии)
    # Сокращаю для краткости - скопируйте из прошлого кода

if __name__ == '__main__':
    print("🚀 FunPay Support Bot запущен!")
    bot.polling(none_stop=True)
