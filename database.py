import json
import aiosqlite
from pathlib import Path

class Database:
    def __init__(self, db_path: str = "filters.db"):
        # Создаем директорию data если её нет
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        
        # Используем путь внутри директории data
        self.db_path = str(data_dir / db_path)

    async def init_db(self):
        """Initialize database tables."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS filters (
                    word TEXT PRIMARY KEY,
                    message_data TEXT
                )
            ''')
            await db.commit()

    async def load_filters(self):
        """Load all filters from database."""
        await self.init_db()
        filters = {}
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute('SELECT word, message_data FROM filters') as cursor:
                async for word, message_data in cursor:
                    filters[word] = json.loads(message_data)
        return filters

    async def save_filter(self, word: str, message_data: dict):
        """Save a single filter to database."""
        await self.init_db()
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                'INSERT OR REPLACE INTO filters (word, message_data) VALUES (?, ?)',
                (word, json.dumps(message_data))
            )
            await db.commit()

    async def delete_filter(self, word: str):
        """Delete a filter from database."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('DELETE FROM filters WHERE word = ?', (word,))
            await db.commit()

    async def clear_filters(self):
        """Delete all filters from database."""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('DELETE FROM filters')
            await db.commit() 