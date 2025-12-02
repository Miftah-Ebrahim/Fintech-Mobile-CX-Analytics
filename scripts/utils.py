import logging
import sys


def setup_logging(name: str) -> logging.Logger:
    """
    Configures and returns a standard logger.
    Ensures consistent logging format across all scripts.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    return logging.getLogger(name)
