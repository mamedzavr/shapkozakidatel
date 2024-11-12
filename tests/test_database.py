import os
import pytest
import json
from database import Database

@pytest.fixture
def test_db_path():
    return "test_filters.db"

@pytest.fixture
async def database(test_db_path):
    db = Database(db_path=test_db_path)
    await db.init_db()
    yield db
    # Cleanup after tests
    if os.path.exists(test_db_path):
        os.remove(test_db_path)

@pytest.mark.asyncio
async def test_init_db(database):
    # Ensure the database is initialized without errors
    await database.init_db()

@pytest.mark.asyncio
async def test_save_and_load_filter(database):
    filter_word = "test"
    message_data = {"text": "This is a test message"}
    
    await database.save_filter(filter_word, message_data)
    filters = await database.load_filters()
    
    assert filter_word in filters
    assert filters[filter_word] == message_data

@pytest.mark.asyncio
async def test_delete_filter(database):
    filter_word = "test"
    message_data = {"text": "This is a test message"}
    
    await database.save_filter(filter_word, message_data)
    await database.delete_filter(filter_word)
    filters = await database.load_filters()
    
    assert filter_word not in filters

@pytest.mark.asyncio
async def test_clear_filters(database):
    await database.save_filter("test1", {"text": "Message 1"})
    await database.save_filter("test2", {"text": "Message 2"})
    
    await database.clear_filters()
    filters = await database.load_filters()
    
    assert len(filters) == 0 