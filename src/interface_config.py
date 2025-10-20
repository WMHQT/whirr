import json
from pathlib import Path

CONFIG_FILE = Path(__file__).resolve().parent.parent / "interface_config.json"

def load_interface_id() -> int | None:
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)
            return config.get("interface_id")
    except FileNotFoundError:
        print(f" Not found {CONFIG_FILE}")
    except json.JSONDecodeError:
        print(f"File {CONFIG_FILE} is corrupted")
    return None