#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click
from click_aliases import ClickAliasedGroup

from cliai.core import converse, initiate



@click.group(cls=ClickAliasedGroup, invoke_without_command=True)
def cli():
    pass


@cli.command(name='converse', aliases=['chat'])
@click.option('--api', help='Specify an API')
@click.option('--verbose', '-v', is_flag=True, help='Turn on verbose output')
def converse_command(api, verbose):
    """
    Start conversation
    """
    initiate(api)
    converse(verbose=verbose)


# cli.add_command(converse_command)

if __name__ == '__main__':
    cli()
