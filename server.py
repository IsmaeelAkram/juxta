from flask import Flask
import log
import os

app = Flask(__name__)


@app.route("/")
def index():
    return "This endpoint is to ensure the bot is up and running"


def run():
    app.run(port=(os.getenv("PORT") or 8080))
    log.good("Started Flask")