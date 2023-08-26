import config
import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
bot = Bot(token=config.token)
dip = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)
