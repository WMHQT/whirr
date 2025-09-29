import sounddevice as sd
import json
import os

from config import AudioConfig


def load_interface_config(config_path: str = AudioConfig.INTERFACE_CONFIG_PATH):
    """Read the active interface configuration from JSON file.
    Returns dict with interface_id or empty dict if not configured."""
    
    if not os.path.exists(config_path):
        return None
    
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            config = json.load(file)
        
        if 'interface_id' not in config:
            return None
        else:
            return config
    
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in config file: {e}")
        return None
    except PermissionError as e:
        print(f"Permission denied reading config file: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error reading config: {e}")
        return None


def set_interface_config(
        device_index: int,
        config_path: str = AudioConfig.INTERFACE_CONFIG_PATH
) -> None:
    data = {"interface_id": device_index}
    with open(config_path, 'w', encoding='utf-8') as file:
        json.dump(data, file)


def format_microphones_output(
        devices: dict,
        active_indicator: bool = False,
        active_id: int = None
) -> str:
    """Format microphones data for display."""
    if not devices:
        return "No microphones found"
    
    result = []
    separator = "-" * 25

    for device in devices:
        index = device['index']
        mark = "  (*)" if active_indicator and index == active_id else ""
        index_line = f"  Index       : {index}{mark}"

        result.extend([
            index_line,
            f"  Device Name : {device['name']}",
            f"  Sample Rate : {device['default_samplerate']}",
            f"  Channels    : {device['max_input_channels']}",
            separator
        ])

    return "\n".join(result)


def list_microphones(active_only: bool = False) -> str:
    config = load_interface_config()
    active_id = config["interface_id"] if config else None

    try:
        if active_only:
            devices = [sd.query_devices(active_id)]
        else:
            devices = [d for d in sd.query_devices()]
    except Exception as e:
        return f"Error querying devices: {e}"
    
    active_indicator = not active_only

    return format_microphones_output(devices, active_indicator, active_id)


def set_microphones(device_index: int) -> str:
    set_interface_config(device_index)
    return list_microphones(True)


if __name__ == "__main__":
    list_microphones()