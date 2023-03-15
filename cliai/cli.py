#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click
from click_aliases import ClickAliasedGroup

from cliai.core import converse, initiate, manage_config, manage_convos
import os


@click.group(cls=ClickAliasedGroup, invoke_without_command=True)
def cli():
    pass


@cli.command(name='chat', aliases=['converse'])
@click.option('--api-key',
              default=lambda: os.environ.get('OPENAI_API_KEY', ''),
              help='Specify an API key')
@click.option('--api-base',
              default=lambda: os.environ.get('OPENAI_API_BASE', ''),
              help='Use a custom API base')
@click.option('--verbose', '-v', is_flag=True, help='Turn on verbose output')
def converse_command(api_key, api_base, verbose):
    """
    Start conversation
    """
    initiate(api_key, api_base)
    converse(verbose=verbose)


@cli.command(name='config')
def config_command():
    manage_config()


def interactive():
    """
    Enters interactive mode (TUI)
    """
    pass


if __name__ == '__main__':
    cli()
