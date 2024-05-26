from logging.config import dictConfig


class LogConfig:
    """Logging configuration to be set for the server"""

    version = 1

    disable_existing_loggers = False

    formatters = {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
        "access": {
            "format": '%(message)s',
        },
    }

    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    }

    loggers = {
        "": {
            "handlers": ["default"],
            "level": "INFO",
        },
        "uvicorn.error": {
            "level": "INFO",
        },
        "uvicorn.access": {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": False,
        },
    }


def setup_logging():
    dictConfig(LogConfig.__dict__)
