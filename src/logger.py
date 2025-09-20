import atexit
import json
import logging.config
from pathlib import Path

from config import LogsConfig


system_logger: logging.Logger = logging.getLogger("system")
model_logger: logging.Logger = logging.getLogger("model")


def load_log_config(config_path: str = LogsConfig.LOG_CONFIG_PATH) -> dict:
    with open(config_path) as file:
        return json.load(file)


def start_queue_handler(queue_handler: logging.Handler) -> None:
    queue_handler.listener.start()
    atexit.register(queue_handler.listener.stop)

def create_logs_directory(logs_path: str="logs") -> None:
    logs_dir = Path(logs_path)
    if not logs_dir.exists():
        logs_dir.mkdir(parents=True, exist_ok = True)
        system_logger.info(f'Created logs directory" {logs_dir.absolute()}')

def setup_logging() -> None:
    create_logs_directory()
    config = load_log_config()
    logging.config.dictConfig(config)
    system_queue = logging.getHandlerByName("system_queue")
    model_queue = logging.getHandlerByName("model_queue")
    start_queue_handler(system_queue)
    start_queue_handler(model_queue)

