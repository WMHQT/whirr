import sounddevice as sd


def list_microphones() -> None:
    s = sd.query_devices()
    for i, v in enumerate(s):
        device_info = v
        if int(device_info['max_input_channels']):
            print(f"  Index       : {i}")
            print(f"  Device Name : {device_info['name']}")
            print(f"  Sample Rate : {device_info['default_samplerate']}")
            print(f"  Channels    : {device_info['max_input_channels']}")
            print("-" * 25)


def set_microphones(device_index: int) -> None:
    ...


if __name__ == "__main__":
    list_microphones()