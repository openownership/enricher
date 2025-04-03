import click
from enricher.cli.config import get, set, validate
from enricher.cli.enrich import start, setup, reset


@click.group()
def main():
    pass


@click.group()
def config():
    pass


@click.group()
def enrich():
    pass


config.add_command(get)
config.add_command(set)
config.add_command(validate)

enrich.add_command(setup)
enrich.add_command(reset)
enrich.add_command(start)

main.add_command(config)
main.add_command(enrich)

if __name__ == "__main__":
    main()
