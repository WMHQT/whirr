import sounddevice as sd
import numpy as np
from numpy.typing import NDArray

from .broker import setup_broker, stop_channel_processes
from .utils.configure_mics import load_interface_config
from .utils.preprocess_audio import convert_time_series_to_spectogram
from .collect import InferenceResult, get_collector

from . import inference
from .config import (
    AudioConfig,
    LogsConfig,
)


def init_stream(device_index: int | None = None) -> sd.InputStream:
    return sd.InputStream(
        samplerate=AudioConfig.SAMPLE_RATE,
        channels=AudioConfig.CHANNELS,
        dtype=AudioConfig.FORMAT,
        blocksize=AudioConfig.CHUNK_SIZE,
        device=device_index
    )


def record_continously(stream: sd.InputStream) -> None:
    total_chunks = int((AudioConfig.SAMPLE_RATE / AudioConfig.CHUNK_SIZE) * 2)

    with stream as s:
        try:
            while True:
                time_series = read_audio_chunk(stream, total_chunks)
                inference.do_inference(time_series)
        except KeyboardInterrupt:
            print("\nStop recording...")
    
    save_to_wav()


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
    config = load_interface_config()
    device_id = config["interface_id"]
    input_queues, result_queue, processes, collector = setup_broker()  # ⭐ ОБНОВИТЬ

    try:
        stream = init_stream(device_id)
        record_continously(stream, input_queues, result_queue)
    except RuntimeError as e:
        print(e)
        return None
    finally:
        if collector:
            collector.stop()
        stop_channel_processes(processes, input_queues)


def do_inference(time_series: NDArray, channel_id: int = 0) -> None:
    spectogram = convert_time_series_to_spectogram(time_series)
    processed_audio = np.expand_dims(spectogram, axis=(-1, 0))
    category_pred, target_pred = inference.make_prediction(processed_audio)

    # ⭐ ДОБАВИТЬ ЭТО - отправка в коллектор
    from collect import get_collector
    from collect import InferenceResult
    import time

    collector = get_collector()
    if collector:
        result = InferenceResult(
            channel_id=channel_id,
            timestamp=time.time(),
            category_pred=category_pred,
            target_pred=target_pred
        )
        # Нужно отправить в result_queue коллектора
        # Это требует доработки broker.py

    inference.display_prediction(category_pred, target_pred)