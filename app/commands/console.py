import click


class Console:
    """Output styling for the command line."""

    def __init__(self, err: bool = True):
        self.__err = err

    def info(self, message, **kwargs):
        click.secho(message, fg='green', err=self.__err, **kwargs)

    def error(self, message, **kwargs):
        click.secho(message, fg='bright_red', err=self.__err, **kwargs)

    def notice(self, message, **kwargs):
        click.secho(message, fg='bright_green', err=self.__err, **kwargs)

    def text(self, message, **kwargs):
        click.secho(message, err=self.__err, **kwargs)

    def warning(self, message, **kwargs):
        click.secho(message, fg='yellow', err=self.__err, **kwargs)
