from flask import Flask
import log

app = Flask(__name__)


@app.route("/")
def index():
    return "This endpoint is to ensure the bot is up and running"


def run():
    app.run()
    log.good("Started Flask")