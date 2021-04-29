from dotenv import load_dotenv

load_dotenv()

from juxta import Juxta
import asyncio
import signal
import log
import os


token = os.getenv("TOKEN")
bot = Juxta()
bot.run(token)