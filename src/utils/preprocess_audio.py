import librosa
import numpy as np
from numpy.typing import NDArray

from config import AudioConfig, InferenceConfig


def read_time_series_from_buffer(frames: bytes) -> NDArray:
    time_series = np.frombuffer(frames, dtype=np.int16)
    time_series = time_series.reshape(-1, 2).mean(axis=1)
    time_series = time_series.astype(np.float32) / np.iinfo(np.int16).max
    
    return time_series


def convert_time_series_to_spectogram(time_series: NDArray) -> NDArray:
    time_series = time_series.reshape(-1, 2).mean(axis=1)
    time_series = time_series.astype(np.float32) / np.iinfo(np.int16).max
    spectogram = librosa.feature.melspectrogram(
        y=time_series,
        sr=AudioConfig.SAMPLE_RATE,
        n_mels=InferenceConfig.N_MELS,
        fmax=InferenceConfig.FMAX,
    )
    spectogram = librosa.power_to_db(spectogram, ref=np.max)
    adjusted_spectogram = _adjust_spectogram(spectogram)

    return adjusted_spectogram


def _adjust_spectogram(spectogram: NDArray) -> NDArray:
    target_width = InferenceConfig.TARGET_SHAPE[1]
    current_width = spectogram.shape[1]
    current_height = spectogram.shape[0]

    if current_width == target_width:
        return spectogram

    adjusted_spectogram = np.zeros(
        (current_height, target_width), dtype=spectogram.dtype
    )
    copy_cols = min(current_width, target_width)
    adjusted_spectogram[:, :copy_cols] = spectogram[:, :copy_cols]

    return adjusted_spectogram
