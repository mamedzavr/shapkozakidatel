from telegram import Update, Message
from telegram.ext import ContextTypes
from typing import Dict
from database import Database

class FilterManager:
    def __init__(self, db_path: str = "filters.db"):
        self.db = Database(db_path)
        self.filter_messages: Dict[str, dict] = {}

    async def _load_filters(self):
        """Load filters from database."""
        self.filter_messages = await self.db.load_filters()

    async def add_filter(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Add a new filter based on a replied message."""
        if not update.message.reply_to_message:
            await update.message.reply_text('Эта команда должна быть ответом на сообщение!')
            return

        if not context.args:
            await update.message.reply_text('Укажите слово для фильтра! Пример: /filter привет')
            return

        filter_word = context.args[0].lower()
        message = update.message.reply_to_message
        
        # Convert Message object to serializable format
        filter_data = {
            'message_id': message.message_id,
            'chat_id': message.chat_id,
        }
        
        # Save different types of content
        if message.text:
            filter_data['text'] = message.text
        if message.photo:
            filter_data['photo'] = message.photo[-1].file_id
        if message.video:
            filter_data['video'] = message.video.file_id
        if message.animation:
            filter_data['animation'] = message.animation.file_id
        if message.sticker:
            filter_data['sticker'] = message.sticker.file_id
        if message.voice:
            filter_data['voice'] = message.voice.file_id
        if message.audio:
            filter_data['audio'] = message.audio.file_id
        if message.document:
            filter_data['document'] = message.document.file_id
        if message.caption:
            filter_data['caption'] = message.caption

        # Save to both memory and database
        self.filter_messages[filter_word] = filter_data
        await self.db.save_filter(filter_word, filter_data)
        
        await update.message.reply_text(f'Фильтр "{filter_word}" успешно добавлен!')

    async def check_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Check if message contains any filter words and respond accordingly."""
        if not update.message or not update.message.text:
            return

        # Ensure filters are loaded
        await self._load_filters()

        message_text = update.message.text.lower()
        for filter_word, stored_message in self.filter_messages.items():
            if filter_word in message_text:
                try:
                    # Send content based on type
                    if stored_message.get('text'):
                        await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=stored_message['text']
                        )
                    if stored_message.get('photo'):
                        await context.bot.send_photo(
                            chat_id=update.effective_chat.id,
                            photo=stored_message['photo'],
                            caption=stored_message.get('caption')
                        )
                    if stored_message.get('video'):
                        await context.bot.send_video(
                            chat_id=update.effective_chat.id,
                            video=stored_message['video'],
                            caption=stored_message.get('caption')
                        )
                    if stored_message.get('animation'):
                        await context.bot.send_animation(
                            chat_id=update.effective_chat.id,
                            animation=stored_message['animation'],
                            caption=stored_message.get('caption')
                        )
                    if stored_message.get('sticker'):
                        await context.bot.send_sticker(
                            chat_id=update.effective_chat.id,
                            sticker=stored_message['sticker']
                        )
                    if stored_message.get('voice'):
                        await context.bot.send_voice(
                            chat_id=update.effective_chat.id,
                            voice=stored_message['voice'],
                            caption=stored_message.get('caption')
                        )
                    if stored_message.get('audio'):
                        await context.bot.send_audio(
                            chat_id=update.effective_chat.id,
                            audio=stored_message['audio'],
                            caption=stored_message.get('caption')
                        )
                    if stored_message.get('document'):
                        await context.bot.send_document(
                            chat_id=update.effective_chat.id,
                            document=stored_message['document'],
                            caption=stored_message.get('caption')
                        )
                except Exception as e:
                    # If sending fails, remove the filter
                    del self.filter_messages[filter_word]
                    await self.db.delete_filter(filter_word)

    async def show_filters(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show all active filters."""
        # Ensure filters are loaded
        await self._load_filters()

        if not self.filter_messages:
            await update.message.reply_text('Список фильтров пуст!')
            return

        filter_list = '\n• '.join(sorted(self.filter_messages.keys()))
        await update.message.reply_text(f'Список активных фильтров:\n• {filter_list}')

    def get_filters(self):
        """Return the current filter dictionary."""
        return self.filter_messages

    async def clear_filters(self):
        """Clear all filters."""
        self.filter_messages.clear()
        await self.db.clear_filters()