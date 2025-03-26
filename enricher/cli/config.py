import click
import yaml
from typing import Any, Dict, List, Optional

DEFAULT_CONFIG = "config.yaml"


def read_config(config_path: str) -> Dict[str, Any]:
    with open(config_path, "r") as file:
        return yaml.safe_load(file) or {}


def write_config(config_path: str, config_data: Dict[str, Any]) -> None:
    with open(config_path, "w") as file:
        yaml.safe_dump(config_data, file)


def get_nested(config_data: Dict[str, Any], keys: List[str]) -> Optional[str]:
    value: Dict | str | None = config_data
    for key in keys:
        if value is None:
            return None
        if not isinstance(value, dict):
            return value
        value = value.get(key, None)
    return value


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


def get_value(config: str = DEFAULT_CONFIG, key: str | None = "") -> Optional[str]:
    config_data = read_config(config)
    if key is None:
        return None
    keys = key.split(".")
    return get_nested(config_data, keys) or None


@click.command()
@click.option("--config", default=DEFAULT_CONFIG, help="Path to the config file")
@click.argument("key")
def get(config: str, key: str | None = None) -> str | None:
    value = get_value(config, key)
    if value is not None:
        click.echo(f"{key}: {value}")
    else:
        click.echo(f"{key} not found in the configuration")
    return value


@click.command()
@click.option("--config", default="config.yaml", help="Path to the config file")
@click.argument("key")
@click.argument("value", required=False)
def set(config: str, key: str, value: str | None = None) -> None:
    config_data = read_config(config)
    keys = key.split(".")
    set_nested(config_data, keys, value)
    write_config(config, config_data)
    if value is None:
        click.echo(f"Removed {key} from the configuration")
    else:
        click.echo(f"Set {key} to {value} in the configuration")


@click.command()
@click.option("--config", default="config.yaml", help="Path to the config file")
def validate(config: str) -> bool:
    required_keys = ["source", "enrichment", "source.es.index"]
    for key in required_keys:
        if not get_value(config, key):
            click.echo("Configuration is invalid.")
            return False
    click.echo("Configuration is valid.")
    return True

