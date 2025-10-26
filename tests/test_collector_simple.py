import sys
import os
import time
import queue
import logging

# Добавляем корень проекта в путь
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.collect import ResultCollector, InferenceResult
from src.logger import setup_logging


def test_collector_simple():
    """Простой тест коллектора"""
    # Сначала настраиваем логирование
    setup_logging()

    # Создаем коллектор напрямую
    test_queue = queue.Queue()
    collector = ResultCollector(test_queue)
    collector.start()

    # Отправляем синхронизированные данные
    timestamp = time.time()
    for i in range(8):
        result = InferenceResult(
            channel_id=i,
            timestamp=timestamp,
            category_pred=(i % 5, 0.9),
            target_pred=(i % 7, 0.8)
        )
        test_queue.put(result)

    # Ждем обработки
    time.sleep(2)

    # Проверяем статус
    status = collector.get_status()
    collector.stop()

    assert status['pending_sets'] == 0, "Должны быть обработаны все наборы"
    assert status['processed_count'] == 8, "Должны быть обработаны все каналы"
    print("✅ Тест пройден!")


if __name__ == "__main__":
    test_collector_simple()