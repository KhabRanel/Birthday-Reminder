import django_setup  # ВАЖНО: должен быть ПЕРВЫМ импортом!
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config_data.config import BOT_TOKEN
from handlers import user_handlers


async def main():
    """
    Главная функция бота.
    Создает экземпляры Bot и Dispatcher, запускает поллинг.
    """
    # Создаем бота с токеном
    bot = Bot(token=BOT_TOKEN)

    # Создаем диспетчер с хранилищем состояний в памяти
    dp = Dispatcher(storage=MemoryStorage())

    # Подключаем роутер с хэндлерами
    dp.include_router(user_handlers.router)

    # Запускаем поллинг (получение обновлений от Telegram)
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())