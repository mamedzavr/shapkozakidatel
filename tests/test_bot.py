import pytest
from unittest.mock import AsyncMock, patch
from telegram import Update, User
from telegram.ext import ContextTypes
from bot import start

@pytest.fixture
def update():
    update = AsyncMock(spec=Update)
    update.effective_user = AsyncMock(spec=User)
    update.effective_user.username = "test_user"
    update.message = AsyncMock()
    return update

@pytest.fixture
def context():
    return AsyncMock(spec=ContextTypes.DEFAULT_TYPE)

@pytest.mark.asyncio
async def test_start_command(update, context):
    await start(update, context)
    update.message.reply_text.assert_called_once_with(
        'Привет! Я бот-фильтр. Используй команду /filter <слово> в ответ на сообщение, чтобы создать фильтр.'
    )