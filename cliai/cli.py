#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click
from click_aliases import ClickAliasedGroup

from cliai.core import converse, initiate



@click.group(cls=ClickAliasedGroup, invoke_without_command=True)
def cli():
    pass


@cli.command(name='chat', aliases=['converse'])
@click.option('--api', help='Specify an API')  # --api-key, and should be for all
@click.option('--verbose', '-v', is_flag=True, help='Turn on verbose output')
def converse_command(api, verbose):
    """
    Start conversation
    """
    initiate(api)
    converse(verbose=verbose)

def interactive():
    """
    Enters interactive mode (TUI)
    """
    pass


# cli.add_command(converse_command)

if __name__ == '__main__':
    cli()
