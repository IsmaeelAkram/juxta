from dotenv import load_dotenv

load_dotenv()

from juxta import Juxta
import os
import log
import sentry_sdk
import discord
from sentry_sdk.integrations.redis import RedisIntegration

sentry_sdk.init(
    os.getenv("SENTRY_URL"),
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
    integrations=[RedisIntegration()],
)
log.good("Connected to Sentry")

token = os.getenv("TOKEN")
bot = Juxta(intents=discord.Intents.all())
bot.run(token)