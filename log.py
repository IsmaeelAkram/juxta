import chalk
import datetime


def good(x):
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[👍][{current_time}] {chalk.green(x)}")


def danger(x):
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[👎][{current_time}] {chalk.red(x)}")


def warning(x):
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[📄][{current_time}] {chalk.yellow(x)}")


def info(x):
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[📣][{current_time}] {chalk.blue(x)}")