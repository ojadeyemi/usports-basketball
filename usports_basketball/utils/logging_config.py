import logging
import os


def setup_logging():
    """Sets up logging configurations."""
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()  # Default to INFO if LOG_LEVEL is not set

    logging.basicConfig(
        level=getattr(logging, log_level, logging.INFO),  # Set the logging level from env variable
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),  # Output logs to the console
        ],
        datefmt="%d/%m/%Y %H:%M:%S",
    )
