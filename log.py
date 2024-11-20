import sys
import logging


def getLogger(logger_name: str) -> logging.Logger:
    logger = logging.getLogger(logger_name)
    logLevel = logging.getLevelName(logging.DEBUG)
    logger.setLevel(logLevel)

    # Create handlers for logging to the standard output and a file
    stdoutHandler = logging.StreamHandler(stream=sys.stdout)
    fileHandler = logging.FileHandler("tidb-evaluation.log")

    # Set the log levels on the handlers
    stdoutHandler.setLevel(logLevel)
    fileHandler.setLevel(logLevel)

    # Create a log format using Log Record attributes
    fmt = logging.Formatter(
        "%(name)s: %(asctime)s | %(levelname)s | %(filename)s:%(lineno)s | %(process)d >>> %(message)s"
    )

    # Set the log format on each handler
    stdoutHandler.setFormatter(fmt)
    fileHandler.setFormatter(fmt)

    # Add each handler to the Logger object
    logger.addHandler(stdoutHandler)
    logger.addHandler(fileHandler)

    return logger
