import sounddevice as sd
import numpy as np
from numpy.typing import NDArray
import wave
from interface_config import load_interface_id

import inference
from config import (
    AudioConfig,
    LogsConfig,
)


def init_stream(device_index: int | None = None) -> sd.InputStream:
    try:
        devices = sd.query_devices()
        if device_index is not None:
            if device_index < 0 or device_index >= len(devices):
                raise ValueError(f"Device with id={device_index} is unavailable")
        return sd.InputStream(
            samplerate=AudioConfig.SAMPLE_RATE,
            channels=AudioConfig.CHANNELS,
            dtype=AudioConfig.FORMAT,
            blocksize=AudioConfig.CHUNK_SIZE,
            device=device_index,
        )
    except Exception as e:
        raise RuntimeError(f"Audio stream initialization error: {e}")



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
    device_id = load_interface_id()
    print(f"[INFO] Using device: {device_id}")
    try:
        stream = init_stream(device_id)
    except RuntimeError as e:
        print(e)
        return
    record_continously(stream)
