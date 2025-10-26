import time
import numpy as np
import logging
from multiprocessing import Queue

from inference import do_inference
from collect import InferenceResult


def process_channel(channel_id: int, input_queue: Queue, result_queue: Queue) -> None:
    # Обрабатывает аудиоданные из входной очереди канала.

    # Инициализация логгера для процесса
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(f"channel_{channel_id}")

    while True:
        try:
            data = input_queue.get()
            if data is None:  # Сигнал завершения
                logger.info(f"Channel {channel_id} received stop signal")
                break

            timestamp, audio_chunk = data

            start_time = time.time()
            logger.debug(f"Channel {channel_id} started processing")

            # Выполнение инференса
            category_pred, target_pred = do_inference(audio_chunk)

            inference_time = time.time() - start_time
            logger.info(f"Channel {channel_id} inference time: {inference_time:.4f}s")

            # Отправка результата в коллектор
            inference_result = InferenceResult(
                channel_id=channel_id,
                timestamp=timestamp,
                category_pred=category_pred,
                target_pred=target_pred
            )
            result_queue.put(inference_result)

        except Exception as e:
            logger.error(f"Channel {channel_id} error: {e}")