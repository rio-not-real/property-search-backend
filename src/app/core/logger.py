import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "stream": "ext://sys.stdout",
        },
        "stderr": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "stream": "ext://sys.stderr",
            "level": "WARNING",
        },
    },
    "loggers": {"root": {"level": "DEBUG", "handlers": ["stdout", "stderr"]}},
}


def setup_logging() -> None:
    """Setup logging configuration."""

    logging.config.dictConfig(LOGGING_CONFIG)
