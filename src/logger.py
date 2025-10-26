# src/logger.py - ИСПРАВЛЕННАЯ ВЕРСИЯ С КОДИРОВКОЙ
import atexit
import json
import logging.config
from pathlib import Path

# УНИВЕРСАЛЬНЫЙ ИМПОРТ
try:
    from .config import LogsConfig
except ImportError:
    import sys
    import os

    src_path = os.path.join(os.path.dirname(__file__))
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    from config import LogsConfig

system_logger: logging.Logger = logging.getLogger("system")
model_logger: logging.Logger = logging.getLogger("model")


def load_log_config(config_path: str = LogsConfig.LOG_CONFIG_PATH) -> dict:
    # ⭐ ИСПРАВЛЕННАЯ КОДИРОВКА UTF-8
    with open(config_path, 'r', encoding='utf-8') as file:
        config = json.load(file)

    # Динамически обновляем пути в конфиге
    logs_dir = LogsConfig.LOGS_DIR_PATH
    config['handlers']['system_file']['filename'] = str(logs_dir / "system.log.jsonl")
    config['handlers']['model_file']['filename'] = str(logs_dir / "model.log.jsonl")

    # ⭐ ДОБАВЛЯЕМ КОДИРОВКУ ДЛЯ ФАЙЛОВЫХ ОБРАБОТЧИКОВ
    config['handlers']['system_file']['encoding'] = 'utf-8'
    config['handlers']['model_file']['encoding'] = 'utf-8'

    return config


def create_logs_directory(logs_dir: Path = LogsConfig.LOGS_DIR_PATH) -> None:
    if not logs_dir.exists():
        logs_dir.mkdir(parents=True, exist_ok=True)
        print(f'Created logs directory: {logs_dir.absolute()}')


def setup_logging() -> None:
    create_logs_directory()
    try:
        config = load_log_config()

        print(f"🔧 Настройка логирования:")
        print(f"   Папка логов: {LogsConfig.LOGS_DIR_PATH}")
        print(f"   Файл system: {config['handlers']['system_file']['filename']}")
        print(f"   Файл model: {config['handlers']['model_file']['filename']}")

        logging.config.dictConfig(config)

        # Проверяем логгеры
        system_logger.info("System logger initialized")
        model_logger.info("Model logger initialized")

        collect_logger = logging.getLogger("model.collect")
        collect_logger.info("Collect logger initialized")

        print("✅ Логирование успешно настроено")

    except Exception as e:
        print(f"❌ Ошибка настройки логирования: {e}")
        import traceback
        traceback.print_exc()

        # FALLBACK с правильными путями и кодировкой
        logs_dir = LogsConfig.LOGS_DIR_PATH
        logs_dir.mkdir(parents=True, exist_ok=True)

        logging.basicConfig(
            level=logging.INFO,
            format='[%(levelname)s|%(name)s]: %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(logs_dir / 'fallback.log', encoding='utf-8')
            ]
        )
        logging.getLogger("system").warning("Using fallback logging configuration")