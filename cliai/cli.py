#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import click
from click_aliases import ClickAliasedGroup

from cliai.core import converse, initiate, manage_config, manage_convos

LATEST_VERSION_URL = 'https://pypi.org/pypi/cliai/json'


def check_version():
    """Check if CliAI is up-to-date."""
    import json

    import requests
    from pkg_resources import get_distribution
    name = 'cliai'

    current_version = get_distribution(name).version
    latest_version = json.loads(requests.get(LATEST_VERSION_URL.format(name)).text)["info"]["version"]

    if current_version != latest_version:
        click.echo("A new version is available. Run 'pip install --upgrade {}' to update.".format(name))

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
    check_version()
    cli()
