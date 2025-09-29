from multiprocessing import Queue
from queue import Empty


def create_queues(channels: int = 8) -> tuple[list[Queue], Queue]:
    input_queues = [Queue(maxsize = 10) for _ in range(channels)]
    result_queue = Queue(maxsize = 100)
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


def is_overloaded(input_queues: list[Queue]) -> bool:
    return any(q.full() for q in input_queues)


def setup_broker():
    ...