import click

@click.command()
@click.option('--gleif_index', default='GLEIF', help='Name of the GLEIF index')
@click.option('--config', default='config.yaml', help='Path to the config file')
def main(gleif_index, config):
    click.echo(f'Index name is {gleif_index}')
    click.echo(f'Config file is {config}')


if __name__ == '__main__':
    main()

