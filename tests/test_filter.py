import pytest
from unittest.mock import AsyncMock, patch
from telegram import Update, User, Message, PhotoSize
from telegram.ext import ContextTypes
from filter import FilterManager

@pytest.fixture
def update():
    update = AsyncMock(spec=Update)
    update.effective_user = AsyncMock(spec=User)
    update.effective_user.username = "test_user"
    update.message = AsyncMock()
    update.effective_chat = AsyncMock()
    update.effective_chat.id = 123456
    return update

@pytest.fixture
def context():
    context = AsyncMock(spec=ContextTypes.DEFAULT_TYPE)
    context.args = []
    return context

@pytest.fixture
async def filter_manager():
    manager = FilterManager(db_path="test_filters.db")
    await manager.db.init_db()
    yield manager
    await manager.db.clear_filters()

@pytest.mark.asyncio
async def test_add_filter_no_reply(update, context, filter_manager):
    update.message.reply_to_message = None
    await filter_manager.add_filter(update, context)
    update.message.reply_text.assert_called_once_with(
        'Эта команда должна быть ответом на сообщение!'
    )

@pytest.mark.asyncio
async def test_add_filter_no_args(update, context, filter_manager):
    update.message.reply_to_message = AsyncMock(spec=Message)
    context.args = []
    await filter_manager.add_filter(update, context)
    update.message.reply_text.assert_called_once_with(
        'Укажите слово для фильтра! Пример: /filter привет'
    )

# @pytest.mark.asyncio
# async def test_add_filter_success(update, context, filter_manager):
#     update.message.reply_to_message = AsyncMock(spec=Message)
#     update.message.reply_to_message.text = "Test message"
#     update.message.reply_to_message.message_id = 123
#     update.message.reply_to_message.chat_id = 456
#     update.message.reply_to_message.photo = [PhotoSize(file_id="photo_file_id", file_unique_id="unique_id", width=100, height=100)]
#     context.args = ['тест']
#     await filter_manager.add_filter(update, context)
#     update.message.reply_text.assert_called_once_with(
#         'Фильтр "тест" успешно добавлен!'
#     )

@pytest.mark.asyncio
async def test_check_message_no_trigger(update, context, filter_manager):
    update.message.text = "обычное сообщение"
    await filter_manager.check_message(update, context)
    update.message.reply_text.assert_not_called()

# @pytest.mark.asyncio
# async def test_check_message_with_trigger(update, context, filter_manager):
#     # Add test filter
#     update.message.reply_to_message = AsyncMock(spec=Message)
#     update.message.reply_to_message.text = "Test message"
#     update.message.reply_to_message.message_id = 123
#     update.message.reply_to_message.chat_id = 456
#     update.message.reply_to_message.photo = [PhotoSize(file_id="photo_file_id", file_unique_id="unique_id", width=100, height=100)]
#     context.args = ['тест']
#     await filter_manager.add_filter(update, context)
    
#     # Simulate message that triggers filter
#     update.message.text = "это тестовое сообщение"
#     await filter_manager.check_message(update, context)
#     context.bot.send_message.assert_called_once_with(
#         chat_id=update.effective_chat.id,
#         text="Test message"
#     )

@pytest.mark.asyncio
async def test_show_filters_empty(update, context, filter_manager):
    await filter_manager.show_filters(update, context)
    update.message.reply_text.assert_called_once_with('Список фильтров пуст!')

# @pytest.mark.asyncio
# async def test_show_filters_with_items(update, context, filter_manager):
#     update.message.reply_to_message = AsyncMock(spec=Message)
#     update.message.reply_to_message.text = "Test message"
#     update.message.reply_to_message.message_id = 123
#     update.message.reply_to_message.chat_id = 456
#     update.message.reply_to_message.photo = [PhotoSize(file_id="photo_file_id", file_unique_id="unique_id", width=100, height=100)]
#     context.args = ['тест']
#     await filter_manager.add_filter(update, context)
    
#     await filter_manager.show_filters(update, context)
#     update.message.reply_text.assert_called_once_with('Список активных фильтров:\n• тест')