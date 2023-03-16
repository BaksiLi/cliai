#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
from typing import Dict, Optional

import openai
import questionary as q

from cliai.util import print_success, print_warning

DEFAULT_CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".cliai")


def is_authenticated() -> bool:
    """
    Check if the user has authenticated with OpenAI.
    """
    if openai.api_key:
        try:
            return openai.Model.list() is not None
        except openai.error.AuthenticationError:
            return False
    else:
        return False


def auth(api_key: str, api_base: str = None,
         print_success_msg: Optional[bool] = True,
         verbose: Optional[bool] = False) -> None:
    """
    Authenticate the API key provided by the user.
    """
    if not api_key:
        print_warning('API key cannot be empty!')
        return False
    openai.api_key = api_key

    if api_base:
        print(f'Using custom API base: {api_base}.')
        openai.api_base = api_base

    if is_authenticated():
        if print_success_msg:
            print_success('Authenticated!\n')
        return True
    else:
        print_warning('Incorrect API key provided!')
        return False


def create_or_update_config(config_dir: str = DEFAULT_CONFIG_DIR) -> None:
    """
    Create a new OpenAI configuration file in the specified directory.
    If the directory does not exist, it will be created.
    """
    os.makedirs(config_dir, exist_ok=True)
    config_file = os.path.join(config_dir, 'openai_config.json')

    # Interaction for configs
    print()
    while True:
        api_key = q.password('Enter your OpenAI API key:\n').ask()
        if auth(api_key):
            break

    # Advanced settings
    advanced = q.checkbox('Choose the settings you wish to use:',
                          choices=[q.Choice('API Base URL', 'change_url'),
                                   q.Choice('Organization ID', 'org'),
                                   q.Choice('Member Name', 'name')]
                          ).ask()

    # Validate inputs for api_base, org_id and member_name
    if 'change_url' in advanced:
        api_base = q.text('Enter the base url endpoint: ').ask().strip()

    if 'org' in advanced:
        org_id = q.text('Enter your organization ID: ').ask().strip()

    if 'name' in advanced:
        member_name = q.text('Enter your member name: ').ask().strip()

    print()

    # Save the configurations to the file
    config = {
        "api_key": api_key,
        "api_base": api_base if 'change_url' in advanced else None,
        "organization_id": org_id if 'org' in advanced else None,
        "member_name": member_name if 'name' in advanced else None,
    }

    try:
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=4)
            print_success(f'Config file saved to {config_file}.')
    except Exception as e:
        print_warning(f'Error saving config file to {config_file}. {str(e)}')


def load_config(config_dir: str = DEFAULT_CONFIG_DIR) -> Dict[str, str]:
    """
    Load the OpenAI configurations from a JSON file in the specified directory.
    If the directory or file does not exist, ask to create one.
    """
    config_file = os.path.join(config_dir, 'openai_config.json')

    # Check if the file exists
    if not os.path.isfile(config_file):
        print_warning(f'Config file not found at {config_file}!')
        print('Creating...')
        create_or_update_config(config_dir)

    # Load the configurations from the file
    with open(config_file, 'r') as f:
        try:
            config = json.load(f)
        except json.JSONDecodeError:
            print_warning(
                f'Failed to load config file {config_file}: invalid JSON format.'
            )
            return None

    print()

    return config
