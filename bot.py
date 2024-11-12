from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import os

# Словарь для хранения фильтров и соответствующих сообщений
filter_messages = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Пользователь {update.effective_user.username} запустил бота")
    await update.message.reply_text('Привет! Я бот-фильтр. Используй команду /filter <слово> в ответ на сообщение, чтобы создать фильтр.')

async def add_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        print(f"Пользователь {update.effective_user.username} попытался создать фильтр без ответа на сообщение")
        await update.message.reply_text('Эта команда должна быть ответом на сообщение!')
        return
    
    if len(context.args) < 1:
        print(f"Пользователь {update.effective_user.username} не указал слово для фильтра")
        await update.message.reply_text('Укажите слово для фильтра! Пример: /filter привет')
        return
    
    filter_word = context.args[0].lower()
    filter_messages[filter_word] = update.message.reply_to_message
    
    print(f"Пользователь {update.effective_user.username} создал фильтр '{filter_word}'")
    await update.message.reply_text(f'Фильтр "{filter_word}" успешно добавлен!')

async def check_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = update.message.text.lower()
    
    for filter_word in filter_messages:
        if filter_word in message_text:
            print(f"Сработал фильтр '{filter_word}' на сообщение от {update.effective_user.username}")
            await filter_messages[filter_word].copy(update.effective_chat.id)

def main():
    print("Загрузка конфигурации...")
    load_dotenv()
    
    token = os.getenv('TELEGRAM_TOKEN')
    if not token:
        print("ОШИБКА: Не найден TELEGRAM_TOKEN в файле .env")
        return
    
    print("Инициализация бота...")
    application = Application.builder().token(token).build()
    
    print("Настройка обработчиков команд...")
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('filter', add_filter))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_message))
    
    print("Бот запущен и готов к работе!")
    application.run_polling()

if __name__ == '__main__':
    main()
