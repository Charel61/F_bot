import asyncio
import logging

from aiogram.fsm.storage.redis import RedisStorage, Redis
from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from handlers import handlres
from keyboards.main_menu import set_main_menu



# Инициализируем логгер
logger = logging.getLogger(__name__)

# Функция конфигурирования и запуска бота
async def main():
        # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    redis: Redis = Redis(host='localhost')
       # Инициализируем хранилище (создаем экземпляр класса MemoryStorage)
    storage: RedisStorage = RedisStorage(redis=redis)
    # Загружаем конфиг в переменную config
    config: Config = load_config('.env')
         # Создаем объекты бота и диспетчера
    bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp: Dispatcher = Dispatcher(storage=storage)







    # Регистриуем роутеры в диспетчере
    dp.include_router(handlres.router)

    await set_main_menu(bot)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
