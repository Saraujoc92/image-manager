import logging


LOG_FORMAT_DEBUG = "%(levelname)s:%(message)s:%(pathname)s:%(funcName)s:%(lineno)d"

def configure_logging(log_level: int = logging.INFO) -> None:
    logging.basicConfig(level=log_level, format=LOG_FORMAT_DEBUG)