import logging


logger = logging.getLogger("parser")

logger.level = logging.INFO

console = logging.StreamHandler()
file = logging.FileHandler('app.log', encoding="utf-8")

fmt = logging.Formatter(
    "%(asctime)s - [%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
)

console.setFormatter(fmt)
file.setFormatter(fmt)

logger.addHandler(console)
logger.addHandler(file)