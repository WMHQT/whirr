import sounddevice as sd


def list_microphones(active_only: bool = False, active_id: int = None) -> str:
    result = []
    devices = sd.query_devices()

    for i, device_info in enumerate(devices):
        if int(device_info['max_input_channels']):
            if active_only:
                if i == active_id:
                    result.append(f"  Index       : {i}")
                    result.append(f"  Device Name : {device_info['name']}")
                    result.append(f"  Sample Rate : {device_info['default_samplerate']}")
                    result.append(f"  Channels    : {device_info['max_input_channels']}")
                    result.append("-" * 25)
            else:
                if i == active_id:
                    result.append(f"  Index       : {i}  (*)")
                else:
                    result.append(f"  Index       : {i}  ")
                result.append(f"  Device Name : {device_info['name']}")
                result.append(f"  Sample Rate : {device_info['default_samplerate']}")
                result.append(f"  Channels    : {device_info['max_input_channels']}")
                result.append("-" * 25)
    return "\n".join(result) if result else "No microphones found"


def set_microphones(device_index: int) -> None:
    ...


if __name__ == "__main__":
    list_microphones()