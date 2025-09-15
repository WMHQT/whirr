import logging
from logger import (
    model_logger,
    system_logger
)


def test_system_logger(caplog) -> None:
    with caplog.at_level(logging.INFO):
        system_logger.info("This is log message.")

    assert "This is log message." in caplog.text


def test_model_logger(caplog) -> None:
    with caplog.at_level(logging.INFO):
        model_logger.info("This is log message.")

    assert "This is log message." in caplog.text
