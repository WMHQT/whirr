import sounddevice as sd
import json


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
    s = sd.query_devices()
    for i, v in enumerate(s):
        device_info = v
        if int(device_info['max_input_channels']) and device_info['index'] == device_index[0]:
            print(f"  Index       : {i}")
            print(f"  Device Name : {device_info['name']}")
            print(f"  Sample Rate : {device_info['default_samplerate']}")
            print(f"  Channels    : {device_info['max_input_channels']}")
            print("-" * 25)
        data = {"interface_id": device_index[0]}
        with open("src/utils/interface_config.json", "w", encoding="utf-8") as file:
            json.dump(data, file)

if __name__ == "__main__":
    list_microphones()