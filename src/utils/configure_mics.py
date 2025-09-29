import sounddevice as sd
import json
import os


def read_interface_config():
    '''Read the active interface configuration from JSON file.
    Returns dict with interface_id or empty dict if not configured/invalid.'''
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(current_dir, "interface_config.json")
    
    if not os.path.exists(config_file):
        return {}
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
            if config.get("interface_id"):
                return config
            else:
                return {}
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in config file: {e}")
        return {}
    except PermissionError as e:
        print(f"Permission denied reading config file: {e}")
        return {}
    except Exception as e:
        print(f"Unexpected error reading config: {e}")
        return {}

def get_microphones_data():
    """Get raw microphones data."""
    return sd.query_devices()

def filter_microphones(devices, active_only=False, active_id=None):
    """Filter microphones based on criteria."""
    input_devices = []
    
    for i, device_info in enumerate(devices):
        if int(device_info['max_input_channels']) > 0:
            device_data = {
                'index': i,
                'name': device_info['name'],
                'sample_rate': device_info['default_samplerate'],
                'channels': device_info['max_input_channels'],
                'is_active': (i == active_id)
            }
            input_devices.append(device_data)
    
    if active_only and active_id is not None:
        return [device for device in input_devices if device['is_active']]
    
    return input_devices

def format_microphones_output(devices, show_active_indicator=False):
    """Format microphones data for display."""
    if not devices:
        return "No microphones found"
    
    result = []
    for device in devices:
        if show_active_indicator:
            active_marker = "  (*)" if device['is_active'] else "  "
            result.append(f"  Index       : {device['index']}{active_marker}")
        else:
            result.append(f"  Index       : {device['index']}")
        
        result.append(f"  Device Name : {device['name']}")
        result.append(f"  Sample Rate : {device['sample_rate']}")
        result.append(f"  Channels    : {device['channels']}")
        result.append("-" * 25)
    
    return "\n".join(result)

def list_microphones(active_only: bool = False, active_id: int = None) -> str:
    """Main function to list microphones - combines business logic and presentation."""
    all_devices = get_microphones_data()
    
    filtered_devices = filter_microphones(all_devices, active_only, active_id)
    
    show_active_indicator = not active_only
    return format_microphones_output(filtered_devices, show_active_indicator)

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