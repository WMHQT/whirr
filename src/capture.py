import sounddevice as sd
import numpy as np
from numpy.typing import NDArray
import wave

import inference
from config import (
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
    stream = init_stream()
    record_continously(stream)
