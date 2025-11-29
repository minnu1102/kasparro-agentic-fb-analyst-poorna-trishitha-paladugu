import logging
from rich.logging import RichHandler

def setup_logger(name):
    """
    Configures a professional logger using the Rich library.
    It suppresses noisy logs from external libraries (like HTTP requests)
    so you only see your Agents' activity.
    """
    # Create the configuration
    logging.basicConfig(
        level="INFO",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True, markup=True)]
    )

    # 🤫 Shhh: Silence the noisy background libraries
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.WARNING)

    # Return a logger with the specific agent's name
    return logging.getLogger(name)