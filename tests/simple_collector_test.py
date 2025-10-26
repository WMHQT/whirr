import sys
import os
import time
import queue
import logging

# Простая настройка
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Простые импорты
from src.logger import setup_logging
from src.collect import ResultCollector, InferenceResult


def simple_test():
    print("🧪 ПРОСТОЙ ТЕСТ КОЛЛЕКТОРА")

    # Создаем коллектор напрямую
    test_queue = queue.Queue()
    collector = ResultCollector(test_queue)

    print("1. ✅ Коллектор создан напрямую")

    # Запускаем
    collector.start()
    time.sleep(1)

    print(f"2. ✅ Коллектор запущен")

    # Отправляем данные
    timestamp = time.time()
    for i in range(8):
        result = InferenceResult(
            channel_id=i,
            timestamp=timestamp,
            category_pred=(i, 0.9),
            target_pred=(i, 0.8)
        )
        test_queue.put(result)
        print(f"   📤 Канал {i} отправлен")

    # Ждем
    time.sleep(2)

    # Проверяем
    status = collector.get_status()
    print(f"3. 📊 Статус: {status}")
    print(f"   Обработано: {collector.processed_count}")

    # Останавливаем
    collector.stop()

    success = collector.processed_count == 8
    print(f"\n{'🎉 УСПЕХ' if success else '💥 ОШИБКА'}: Обработано {collector.processed_count}/8 результатов")

    return success


if __name__ == "__main__":
    simple_test()