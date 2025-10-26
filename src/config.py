from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.absolute()  # src -> корень проекта

@dataclass(frozen=True)
class AudioConfig:
    FORMAT: str = "int16"
    SAMPLE_RATE: int = 44100
    SAMPLE_WIDTH: int = 2
    CHANNELS: int = 1
    CHUNK_SIZE: int = 1024
    INTERFACE_CONFIG_PATH: str = str(PROJECT_ROOT / "src" / "utils" / "interface_config.json")

@dataclass(frozen=True)
class InferenceConfig:
    N_MELS: int = 256
    FMAX: int = 16384
    TARGET_SHAPE: tuple = (256, 173)

@dataclass(frozen=True)
class ModelConfig:
    MODELS_PATH: Path = PROJECT_ROOT / "models"
    MODEL_NAME: Path = Path("whirr-1-1.2b.onnx")
    MODEL: str = str(MODELS_PATH / MODEL_NAME)

@dataclass(frozen=True)
class LogsConfig:
    # ⭐ АБСОЛЮТНЫЕ ПУТИ ОТНОСИТЕЛЬНО КОРНЯ ПРОЕКТА
    LOG_CONFIG_PATH: str = str(PROJECT_ROOT / "src" / "log_config.json")
    LOG_RECORD_PATH: str = str(PROJECT_ROOT / "logs" / "record.log.wav")
    LOGS_DIR_PATH: Path = PROJECT_ROOT / "logs"

@dataclass(frozen=True)
class CollectorConfig:
    CHANNELS_COUNT: int = 8
    SYNC_TIMEOUT: float = 2.0
    COLLECT_LOGGER: str = "model.collect"