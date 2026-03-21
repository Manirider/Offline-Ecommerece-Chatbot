import logging
import os
from datetime import datetime


class Logger:
    def __init__(self, log_dir="logs"):
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(
            log_dir, f"chatbot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        )
        self.logger = logging.getLogger(f"ChatbotLogger_{id(self)}")
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            handler = logging.FileHandler(log_file, encoding="utf-8")
            handler.setFormatter(
                logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
            )
            self.logger.addHandler(handler)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)
