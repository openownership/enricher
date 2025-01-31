import yaml
from typing import Any, Dict, List, Optional


def read_config(config_path: str) -> Dict[str, Any]:
    with open(config_path, "r") as file:
        return yaml.safe_load(file) or {}


def write_config(config_path: str, config_data: Dict[str, Any]) -> None:
    with open(config_path, "w") as file:
        yaml.safe_dump(config_data, file)


def get_nested(config_data: Dict[str, Any], keys: List[str]) -> Optional[str]:
    for key in keys:
        config_data = config_data.get(key, None)
        if config_data is None:
            return None
    return config_data


def set_nested(
    config_data: Dict[str, Any], keys: List[str], value: Optional[str]
) -> None:

    for key in keys[:-1]:
        config_data = config_data.setdefault(key, {})
        if value is None:
            config_data.pop(keys[-1], None)
        else:
            config_data[keys[-1]] = value
    print(config_data)
