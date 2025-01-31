import click
from gleif_enricher.config import read_config, write_config, get_nested, set_nested


@click.group()
def main():
    pass


@click.group()
def config():
    pass


@click.command()
@click.option("--config", default="config.yaml", help="Path to the config file")
@click.argument("key")
def get(config: str, key: str or None = None) -> None:
    config_data = read_config(config)
    keys = key.split(".")
    value = get_nested(config_data, keys)
    if value is not None:
        click.echo(f"{key}: {value}")
    else:
        click.echo(f"{key} not found in the configuration")


@click.command()
@click.option("--config", default="config.yaml", help="Path to the config file")
@click.argument("key")
@click.argument("value", required=False)
def set(config: str, key: str, value: str or None = None) -> None:
    config_data = read_config(config)
    keys = key.split(".")
    set_nested(config_data, keys, value)
    write_config(config, config_data)
    if value is None:
        click.echo(f"Removed {key} from the configuration")
    else:
        click.echo(f"Set {key} to {value} in the configuration")


config.add_command(get)
config.add_command(set)
main.add_command(config)

if __name__ == "__main__":
    main()
