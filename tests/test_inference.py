import numpy as np
import wave

from config import AudioConfig
import inference
from utils.preprocess_audio import (
    read_time_series_from_buffer,
    convert_time_series_to_spectogram,
)


TEST_SAMPLE = "tests/car_horn_sample.wav"


def test_make_prediction() -> None:
    def _get_frames(sample_path: str = TEST_SAMPLE) -> bytes:
        with wave.open(sample_path, "rb") as file:
            frames = []
            chunk = file.readframes(AudioConfig.CHUNK_SIZE)
            while chunk:
                frames.append(chunk)
                chunk = file.readframes(AudioConfig.CHUNK_SIZE)
            return b"".join(frames)

    frames = _get_frames()
    time_series = read_time_series_from_buffer(frames)
    spectogram = convert_time_series_to_spectogram(time_series)
    processed_audio = np.expand_dims(spectogram, axis=(-1, 0))
    
    category_pred, target_pred = inference.make_prediction(processed_audio)
    category_label, target_label = 0, 3

    assert category_pred[0] == category_label
    assert target_pred[0] == target_label