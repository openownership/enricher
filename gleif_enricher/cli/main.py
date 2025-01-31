import click
from gleif_enricher.cli.config import get, set
from gleif_enricher.cli.enrich import start, setup


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

enrich.add_command(setup)
enrich.add_command(start)

main.add_command(config)
main.add_command(enrich)

if __name__ == "__main__":
    main()
