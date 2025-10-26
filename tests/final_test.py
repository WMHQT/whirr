# tests/test_logging_fixed.py
import sys
import os
import time
import queue
import json

# Настройка путей
project_root = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(project_root, 'src'))


def test_logging_fixed():
    print("🧪 ТЕСТ ИСПРАВЛЕННОГО ЛОГИРОВАНИЯ")
    print("=" * 45)

    try:
        # Настраиваем логирование
        import logger
        logger.setup_logging()

        # Тестируем коллектор с логированием
        import collect
        import logging

        # Создаем коллектор
        test_queue = queue.Queue()
        collector = collect.ResultCollector(test_queue)
        collector.start()

        print("✅ Коллектор запущен")

        # Отправляем данные
        timestamp = time.time()
        for i in range(8):
            result = collect.InferenceResult(
                channel_id=i,
                timestamp=timestamp,
                category_pred=(i, 0.9),
                target_pred=(i, 0.8)
            )
            test_queue.put(result)

        # Ждем
        time.sleep(2)

        # Проверяем статус
        status = collector.get_status()
        print(f"📊 Статус: {status}")

        # Останавливаем
        collector.stop()

        # ПРОВЕРЯЕМ ЛОГИ
        print("\n📁 ПРОВЕРКА ЛОГОВ:")
        logs_dir = os.path.join(project_root, "logs")

        if os.path.exists(logs_dir):
            # Проверяем все файлы логов
            for log_file in ['model.log.jsonl', 'system.log.jsonl', 'basic.log']:
                file_path = os.path.join(logs_dir, log_file)
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        print(f"📄 {log_file}: {len(lines)} записей")

                        # Ищем логи коллектора
                        if log_file == 'model.log.jsonl':
                            collect_logs = []
                            for line in lines:
                                if 'collect' in line.lower():
                                    collect_logs.append(line)
                            print(f"   🔍 Логов коллектора: {len(collect_logs)}")

                            if collect_logs:
                                print("   📝 Пример лога коллектора:")
                                for log in collect_logs[:2]:
                                    print(f"      {log.strip()}")

        success = status['processed_count'] == 8
        print(f"\n{'🎉 ТЕСТ ПРОЙДЕН' if success else '💥 ТЕСТ НЕ ПРОЙДЕН'}")
        return success

    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    test_logging_fixed()