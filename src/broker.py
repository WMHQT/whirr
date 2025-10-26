from multiprocessing import Queue, Process
from queue import Empty
from typing import List
import time

from process_channel import process_channel
from collect import setup_collector

def create_queues(channels: int = 8) -> tuple[list[Queue], Queue]:
    input_queues = [Queue(maxsize=10) for _ in range(channels)]
    result_queue = Queue(maxsize=100)
    return input_queues, result_queue


def clear_all_queues(input_queues: list[Queue], result_queue: Queue) -> None:
    for q in input_queues:
        while not q.empty():
            try:
                q.get_nowait()
            except Empty:
                break

    while not result_queue.empty():
        try:
            result_queue.get_nowait()
        except Empty:
            break


def start_channel_processes(input_queues: List[Queue], result_queue: Queue) -> List[Process]:
    processes = []
    for channel_id in range(len(input_queues)):
        process = Process(
            target=process_channel,
            args=(channel_id, input_queues[channel_id], result_queue),
            daemon=True
        )
        process.start()
        processes.append(process)
    return processes


def stop_channel_processes(processes: List[Process], input_queues: List[Queue]) -> None:
    # Отправка сигналов завершения
    for queue in input_queues:
        queue.put(None)

    # Ожидание завершения процессов
    for process in processes:
        process.join(timeout=5)
        if process.is_alive():
            process.terminate()


def setup_broker():
    input_queues, result_queue = create_queues()

    collector = setup_collector(result_queue)
    collector.start()

    clear_all_queues(input_queues, result_queue)

    processes = start_channel_processes(input_queues, result_queue)

    time.sleep(2)

    return input_queues, result_queue, processes, collector