import logging
from pathlib import Path
import os


def setup_logging(level="INFO"):
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    numeric_level = getattr(logging, level, logging.INFO)

    logging.basicConfig(
        level=numeric_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / "app.log", encoding='utf-8'),
            logging.StreamHandler()
        ]
    )