from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from utils.db_api import sqlite
from data import config

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

db_users = sqlite.Database()
db_tests = sqlite.Database("data/Tests.db")
db_results = sqlite.Database("data/Results.db")


try:
    db_users.create_table_users()
except :
    pass
try:
    db_tests.create_table_tests()
    db_tests.create_table_fanlar()
except :
    pass
try:
    db_results.create_table_results()
except :
    pass


temp = {}
test_time = {}