import sys
import os
import time

from src.broker import setup_broker

project_root = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(project_root, 'src'))


def test_broker_integration():
    print("🧪 ТЕСТ ИНТЕГРАЦИИ BROKER + COLLECTOR")
    print("=" * 45)

    try:
        # Настраиваем логирование
        import logger
        logger.setup_logging()

        # Это вызовет ошибку, если функции не определены!
        input_queues, result_queue, processes, collector = setup_broker()

        print("✅ Broker запущен с коллектором")
        print(f"   - Очередей: {len(input_queues)}")
        print(f"   - Процессов: {len(processes)}")
        print(f"   - Коллектор работает: {collector._running}")

        # Проверяем статус коллектора
        status = collector.get_status()
        print(f"📊 Статус коллектора: {status}")

        # Останавливаем систему
        collector.stop()

        # Останавливаем процессы
        from broker import stop_channel_processes
        stop_channel_processes(processes, input_queues)

        print("🎉 ИНТЕГРАЦИОННЫЙ ТЕСТ ПРОЙДЕН")
        return True

    except NameError as e:
        print(f"❌ ОШИБКА: Функции не определены в broker.py: {e}")
        return False
    except Exception as e:
        print(f"❌ Другая ошибка: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    test_broker_integration()