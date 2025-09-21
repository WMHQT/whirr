from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AudioConfig:
    FORMAT: str = "int16"
    SAMPLE_RATE: int = 44100
    SAMPLE_WIDTH: int = 2
    CHANNELS: int = 1
    CHUNK_SIZE: int = 1024


@dataclass(frozen=True)
class InferenceConfig:
    N_MELS: int = 256
    FMAX: int = 16384
    TARGET_SHAPE: tuple = (256, 173)


@dataclass(frozen=True)
class ModelConfig:
    MODELS_PATH: Path = Path("models")
    MODEL_NAME: Path = Path("whirr-1-1.2b.onnx")
    MODEL: str = str(MODELS_PATH / MODEL_NAME)


@dataclass(frozen=True)
class LogsConfig:
    LOG_CONFIG_PATH: str = "src/log_config.json"
    LOG_RECORD_PATH: str = "logs/record.log.wav"
    LOGS_DIR_PATH: Path = Path("logs")
