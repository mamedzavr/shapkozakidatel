import pytest
from unittest.mock import AsyncMock, patch
from telegram import Update, User
from telegram.ext import ContextTypes

from bot import start, add_filter, check_message

@pytest.fixture
def update():
    update = AsyncMock(spec=Update)
    update.effective_user = AsyncMock(spec=User)
    update.effective_user.username = "test_user"
    update.message = AsyncMock()
    return update

@pytest.fixture
def context():
    context = AsyncMock(spec=ContextTypes.DEFAULT_TYPE)
    context.args = []
    return context

@pytest.mark.asyncio
async def test_start_command(update, context):
    await start(update, context)
    update.message.reply_text.assert_called_once_with(
        'Привет! Я бот-фильтр. Используй команду /filter <слово> в ответ на сообщение, чтобы создать фильтр.'
    )

@pytest.mark.asyncio
async def test_add_filter_no_reply(update, context):
    update.message.reply_to_message = None
    await add_filter(update, context)
    update.message.reply_text.assert_called_once_with(
        'Эта команда должна быть ответом на сообщение!'
    )

@pytest.mark.asyncio
async def test_add_filter_no_args(update, context):
    update.message.reply_to_message = AsyncMock()
    context.args = []
    await add_filter(update, context)
    update.message.reply_text.assert_called_once_with(
        'Укажите слово для фильтра! Пример: /filter привет'
    )

@pytest.mark.asyncio
async def test_add_filter_success(update, context):
    update.message.reply_to_message = AsyncMock()
    context.args = ['тест']
    await add_filter(update, context)
    update.message.reply_text.assert_called_once_with(
        'Фильтр "тест" успешно добавлен!'
    )

@pytest.mark.asyncio
async def test_check_message_no_trigger(update, context):
    update.message.text = "обычное сообщение"
    await check_message(update, context)
    update.message.copy.assert_not_called()

@pytest.mark.asyncio
async def test_check_message_with_trigger(update, context):
    # Добавляем тестовый фильтр
    test_filter = "тест"
    test_reply = AsyncMock()
    from bot import filter_messages
    filter_messages[test_filter] = test_reply
    
    update.message.text = "это тестовое сообщение"
    update.effective_chat = AsyncMock()
    await check_message(update, context)
    filter_messages[test_filter].copy.assert_called_once_with(
        update.effective_chat.id
    ) 