import sounddevice as sd
import numpy as np
from numpy.typing import NDArray
import wave
import time

import inference
from config import (
    AudioConfig,
    LogsConfig,
)
from broker import setup_broker, stop_channel_processes


def init_stream(device_index: int | None = None) -> sd.InputStream:
    return sd.InputStream(
        samplerate=AudioConfig.SAMPLE_RATE,
        channels=AudioConfig.CHANNELS,
        dtype=AudioConfig.FORMAT,
        blocksize=AudioConfig.CHUNK_SIZE,
        device=device_index
    )


def record_continously(stream: sd.InputStream, input_queues, result_queue) -> None:
    total_chunks = int((AudioConfig.SAMPLE_RATE / AudioConfig.CHUNK_SIZE) * 2)
    channel_counter = 0

    with stream as s:
        try:
            while True:
                timestamp = time.time()
                time_series = read_audio_chunk(stream, total_chunks)
                
                # Циклическое распределение по каналам
                target_queue = input_queues[channel_counter]
                if not target_queue.full():
                    target_queue.put((timestamp, time_series))
                
                channel_counter = (channel_counter + 1) % len(input_queues)
                
                # Неблокирующая проверка результатов
                try:
                    while True:
                        result_timestamp, channel_id, result = result_queue.get_nowait()
                        category_pred, target_pred = result
                        print(f"Channel {channel_id}: {category_pred}, {target_pred}")
                except Empty:
                    continue
                    
        except KeyboardInterrupt:
            print("\nStop recording...")

def read_audio_chunk(stream: sd.InputStream, total_chunks: int) -> NDArray:
    audio_chunks = []
    
    for _ in range(total_chunks):
        chunk, overflow = stream.read(AudioConfig.CHUNK_SIZE)
        # if overflow:
        #     print("Warning: SoundDevice input overflowed")
        audio_chunks.append(chunk)
    time_series = np.concatenate(audio_chunks, axis=0)
    
    return time_series


def save_to_wav(path: str = LogsConfig.LOG_RECORD_PATH) -> None:
    ...
    # with wave.open(path, "wb") as file:
    #     file.setnchannels(AudioConfig.CHANNELS)
    #     file.setsampwidth(AudioConfig.SAMPLE_WIDTH)
    #     file.setframerate(AudioConfig.SAMPLE_RATE)
    #     file.writeframes(b"".join(frames))


def setup_capture() -> None:
    input_queues, result_queue, processes = setup_broker()
    
    try:
        stream = init_stream()
        record_continously(stream, input_queues, result_queue)
    finally:
        # Остановка процессов при завершении
        stop_channel_processes(processes, input_queues)
