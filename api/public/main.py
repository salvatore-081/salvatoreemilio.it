from os import getenv
from multiprocessing import cpu_count
import logging
import sys

from gunicorn.app.base import BaseApplication
from gunicorn.glogging import Logger
from loguru import logger
from graphql import GraphQLError

from core.api import app


LOG_LEVEL = logging.getLevelName(getenv("LOG_LEVEL", "DEBUG"))
JSON_LOGS = True
WORKERS = (cpu_count() * 2) + 1
BIND = f"0.0.0.0:{getenv('GUNICORN_PORT', 14021)}"


class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        message = record.getMessage()
        if record.exc_info:
            etype, _, _ = record.exc_info
            if etype == GraphQLError:
                record.exc_info = None
                message = message.split("\n", 1)[0]
                level = "DEBUG"

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, message)


class StubbedGunicornLogger(Logger):
    def setup(self, cfg):
        handler = logging.NullHandler()
        self.error_logger = logging.getLogger("gunicorn.error")
        self.error_logger.addHandler(handler)
        self.access_logger = logging.getLogger("gunicorn.access")
        self.access_logger.addHandler(handler)
        self.error_logger.setLevel(LOG_LEVEL)
        self.access_logger.setLevel(LOG_LEVEL)


class StandaloneApplication(BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {
            key: value for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


if __name__ == '__main__':
    intercept_handler = InterceptHandler()
    logging.root.setLevel(LOG_LEVEL)

    seen = set()
    for name in [
        *logging.root.manager.loggerDict.keys(),
        "gunicorn",
        "gunicorn.access",
        "gunicorn.error",
        "uvicorn",
        "uvicorn.access",
        "uvicorn.error",
        "ariadne",
    ]:
        if name not in seen:
            seen.add(name.split(".")[0])
            logging.getLogger(name).handlers = [intercept_handler]

    logger.configure(handlers=[{"sink": sys.stdout, "serialize": False}])

    options = {
        "bind": BIND,
        "workers": WORKERS,
        "accesslog": "-",
        "errorlog": "-",
        "worker_class": "uvicorn.workers.UvicornWorker",
        "logger_class": StubbedGunicornLogger
    }

    StandaloneApplication(app, options).run()
