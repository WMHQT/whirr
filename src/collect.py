# collect.py - ИСПРАВЛЕННАЯ ВЕРСИЯ
import queue
import time
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import threading

from src.config import CollectorConfig


@dataclass(frozen=True)
class InferenceResult:
    """Результат инференса для одного канала"""
    channel_id: int
    timestamp: float
    category_pred: Tuple[int, float]
    target_pred: Tuple[int, float]


class ResultCollector:
    def __init__(self, result_queue: queue.Queue, sync_timeout: float = CollectorConfig.SYNC_TIMEOUT):
        self.result_queue = result_queue
        self.sync_timeout = sync_timeout

        # Хранилище неполных наборов
        self.pending_results: Dict[float, Dict[int, InferenceResult]] = {}

        # ИНИЦИАЛИЗАЦИЯ ЛОГГЕРОВ - только ссылки, не используем сразу
        self._system_logger = None
        self._collect_logger = None

        # Управление потоком
        self._running = False
        self._thread: Optional[threading.Thread] = None

        # Для диагностики
        self.processed_count = 0

    @property
    def logger(self):
        """Ленивая инициализация system логгера"""
        if self._system_logger is None:
            self._system_logger = logging.getLogger("system")
        return self._system_logger

    @property
    def collect_logger(self):
        """Ленивая инициализация collect логгера"""
        if self._collect_logger is None:
            self._collect_logger = logging.getLogger(CollectorConfig.COLLECT_LOGGER)
        return self._collect_logger

    def start(self) -> None:
        """Запуск процесса сбора результатов"""
        if self._running:
            return

        self._running = True
        self._thread = threading.Thread(target=self._collect_loop, daemon=True)
        self._thread.start()

        self.logger.info("Result collector started")

    def stop(self) -> None:
        """Остановка процесса сбора результатов"""
        self._running = False
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=5.0)
        self.logger.info("Result collector stopped")

    def _collect_loop(self) -> None:
        """Основной цикл сбора результатов"""
        while self._running:
            try:
                # Чтение из очереди с таймаутом
                result = self.result_queue.get(timeout=1.0)
                self.processed_count += 1

                self._process_single_result(result)
                self._cleanup_expired_results()

            except queue.Empty:
                # Очередь пуста - нормальная ситуация
                continue
            except Exception as e:
                self.logger.error(f"Error in collect loop: {e}")
                time.sleep(0.1)

    def _process_single_result(self, result: InferenceResult) -> None:
        """Обработать один результат инференса"""
        timestamp = result.timestamp

        # Инициализировать набор для этой временной метки
        if timestamp not in self.pending_results:
            self.pending_results[timestamp] = {}

        # Добавить результат в набор
        self.pending_results[timestamp][result.channel_id] = result

        # Проверить, собран ли полный набор
        if len(self.pending_results[timestamp]) == CollectorConfig.CHANNELS_COUNT:
            self._process_complete_set(timestamp)

        # Логировать поступление результата
        self.collect_logger.debug(
            f"Received result - Channel: {result.channel_id}, "
            f"Pending sets: {len(self.pending_results)}"
        )

    def _process_complete_set(self, timestamp: float) -> None:
        """Обработать полный набор из 8 каналов"""
        results = self.pending_results[timestamp]

        # Логировать успешный сбор
        self._log_complete_set(timestamp, list(results.values()))

        # Удалить обработанный набор
        del self.pending_results[timestamp]

    def _cleanup_expired_results(self) -> None:
        """Удалить устаревшие неполные наборы"""
        current_time = time.time()
        expired_timestamps = []

        for timestamp, results in self.pending_results.items():
            # Если набор висит дольше timeout - удаляем
            if current_time - timestamp > self.sync_timeout:
                expired_timestamps.append(timestamp)
                self._log_expired_set(timestamp, results)

        for timestamp in expired_timestamps:
            del self.pending_results[timestamp]

    def _log_complete_set(self, timestamp: float, results: List[InferenceResult]) -> None:
        """Логировать полный набор результатов"""
        # ⭐ ПРОСТОЙ ВАРИАНТ - без extra
        channel_ids = [r.channel_id for r in results]
        categories_info = [
            f"ch{r.channel_id}:cat{r.category_pred[0]}({r.category_pred[1]:.2f})"
            for r in results
        ]

        self.collect_logger.info(
            f"Complete set - Time: {timestamp}, "
            f"Channels: {channel_ids}, "
            f"Categories: {categories_info}"
        )

    def _log_expired_set(self, timestamp: float, results: Dict[int, InferenceResult]) -> None:
        """Логировать удаление устаревшего неполного набора"""
        received = list(results.keys())
        missing = [ch for ch in range(8) if ch not in results]

        self.collect_logger.warning(
            f"Expired set - Time: {timestamp}, "
            f"Received: {received}, Missing: {missing}, "
            f"Timeout: {self.sync_timeout}s"
        )


    def get_status(self) -> Dict:
        """Получить текущий статус коллектора"""
        return {
            "pending_sets": len(self.pending_results),
            "pending_channels": sum(len(channels) for channels in self.pending_results.values()),
            "oldest_timestamp": min(self.pending_results.keys()) if self.pending_results else None,
            "sync_timeout": self.sync_timeout,
            "processed_count": self.processed_count
        }


# Глобальный экземпляр коллектора
_collector: Optional[ResultCollector] = None
_result_queue: Optional[queue.Queue] = None


def setup_collector(result_queue: Optional[queue.Queue] = None) -> ResultCollector:
    global _collector, _result_queue

    if result_queue is None:
        from .broker import create_queues
        _, result_queue = create_queues()

    _result_queue = result_queue
    _collector = ResultCollector(result_queue)
    return _collector


def get_collector() -> Optional[ResultCollector]:
    return _collector


def get_result_queue() -> Optional[queue.Queue]:
    return _result_queue


def start_collection() -> None:
    global _collector
    if _collector is None:
        _collector = setup_collector()
    _collector.start()


def stop_collection() -> None:
    global _collector
    if _collector:
        _collector.stop()