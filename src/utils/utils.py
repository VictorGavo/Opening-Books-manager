# Utility functions (error handling, logging, etc.)
import logging
import sys

def setup_logging(level=logging.INFO):
    """
    Sets up basic logging configuration.
    """

    logger = logging.getLogger()
    logger.setLevel(level)

    # Create a handler to output to the console
    console_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger