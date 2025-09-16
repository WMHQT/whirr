import numpy as np
import onnxruntime as ort
from numpy.typing import NDArray

from config import ModelConfig
from logger import model_logger
from utils.preprocess_audio import convert_time_series_to_spectogram


SESSION = ort.InferenceSession(ModelConfig.MODEL)
INPUT_NAME = SESSION.get_inputs()[0].name


CATEGORY = {
    0: "car",
    1: "emv",
    2: "motorcycle",
    3: "tram",
    4: "truck",
}

TARGET = {
    0: "acceleration",
    1: "bell",
    2: "braking",
    3: "horn",
    4: "idling",
    5: "passing",
    6: "siren",
}


def make_prediction(processed_audio: NDArray) -> tuple[tuple[int, float], tuple[int, float]]:
    predictions = SESSION.run([], {INPUT_NAME: processed_audio})

    category_pred = _get_prediction(predictions[0][0])
    target_pred = _get_prediction(predictions[1][0])

    return (category_pred, target_pred)


def _get_prediction(probs: NDArray) -> tuple[int, float]:
    pred = np.argmax(probs)
    conf = np.round(np.float16(probs[pred]), 4)
    return (pred, conf)


def display_prediction(category_pred: tuple[int, float], target_pred: tuple[int, float]) -> None:
    category_label = CATEGORY.get(category_pred[0])
    target_label = TARGET.get(target_pred[0])

    category_score = category_pred[1]
    target_score = target_pred[1]

    print(f"{category_label:^{12}} - {category_score * 100:^{9}.2f}% | {target_label:^{12}} - {target_score * 100:^{9}.2f}%")
    model_logger.info(f"({category_label}, {category_score:.4f}), ({target_label}, {target_score:.4f})")


def do_inference(time_series: NDArray) -> None:
    spectogram = convert_time_series_to_spectogram(time_series)
    processed_audio = np.expand_dims(spectogram, axis=(-1, 0))
    category_pred, target_pred = make_prediction(processed_audio)
    display_prediction(category_pred, target_pred)
