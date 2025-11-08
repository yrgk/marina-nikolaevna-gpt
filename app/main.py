import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ChatType, ParseMode
from aiogram.client.default import DefaultBotProperties

from .config import CONFIG
from .gpt_service import make_answer

LOG_LEVEL = logging.INFO

# Логгер
logging.basicConfig(level=LOG_LEVEL, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)


# Создаем бота с настройками по умолчанию
bot = Bot(
    token=CONFIG.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# Кешируем username бота
bot_username = None

async def get_bot_username():
    global bot_username
    if bot_username is None:
        bot_me = await bot.get_me()
        bot_username = bot_me.username
        print(f"Бот запущен: @{bot_username}")
    return bot_username

@dp.message(F.content_type == "text")
async def handle_message(message: types.Message):
    # Бот работает только в группах
    if message.chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]:
        return

    username = await get_bot_username()
    mentioned = False
    question_text = ""

    if message.entities:
        for entity in message.entities:
            if entity.type == "mention":
                mention = message.text[entity.offset: entity.offset + entity.length]
                if mention == f"@{username}":
                    mentioned = True
                    question_start = entity.offset + entity.length
                    question_text = message.text[question_start:].strip()
                    break

    if mentioned:
        if not question_text:
            await message.reply("Что спрашиваешь? Иди лучше базу сдавай")
            return

        try:
            processing_msg = await message.reply("Думаю...")

            loop = asyncio.get_event_loop()
            answer = await loop.run_in_executor(None, make_answer, question_text)

            await processing_msg.delete()
            await message.reply(answer)
        except Exception as e:
            error_msg = f"Ошибка при обработке запроса: {str(e)}"
            print(error_msg)
            await message.reply(error_msg)

async def main():
                await get_bot_username()

                await dp.start_polling(
                    bot,
                    allowed_updates=dp.resolve_used_update_types(),
                    polling_timeout=20,
                    request_timeout=20,
                    close_bot_session=True,
                    relax=0.1
                )


if __name__ == "__main__":
    asyncio.run(main())