from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from environs import Env

env = Env()
env.read_env()


bot: Bot = Bot(token=env("BOT_TOKEN"), parse_mode="HTML")
storage = MemoryStorage()
dp: Dispatcher = Dispatcher(storage=storage)