#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import click
from click_aliases import ClickAliasedGroup

from cliai.core import converse, initiate, manage_config, manage_convos


@click.group(cls=ClickAliasedGroup)
def cli():
    pass


@cli.command(name='chat', aliases=['converse'],
             short_help='Interactive Chat Mode')
@click.option('--api-key',
              default=lambda: os.environ.get('OPENAI_API_KEY', ''),
              metavar='<OPENAI_API_KEY>',
              help='Specify an API key')
@click.option('--api-base',
              default=lambda: os.environ.get('OPENAI_API_BASE', ''),
              metavar='<OPENAI_API_BASE>',
              help='Use a custom API base')
@click.option('--verbose', '-v', is_flag=True, help='Turn on verbose output')
@click.option('--stream', is_flag=True, help='Stream output')
def converse_command(api_key, api_base, stream, verbose):
    """
    Start an interactive conversation.
    """
    initiate(api_key, api_base, verbose)
    converse(verbose=verbose, stream=stream)


@cli.command(name='config',
             short_help='Configuration Manager')
def config_command():
    """
    Enter configuration manager.
    """
    manage_config()


def interactive():
    """
    Enter interactive mode (TUI).
    """
    pass


if __name__ == '__main__':
    if len(sys.argv) == 1:
        cli.main(['--help'])
    else:
        cli()
