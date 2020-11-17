import click as click

from sol import Sol


@click.command()
def cli():
    sol = Sol()
    sol.main()


if __name__ == '__main__':
    cli()
