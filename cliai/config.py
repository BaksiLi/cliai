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


def auth(api_key: str, print_success_msg: Optional[bool] = True) -> None:
    """
    Authenticate the API key provided by the user.
    """
    if not api_key:
        print_warning('API key cannot be empty!')
        return False

    openai.api_key = api_key

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

    print()
    # Prompt the user for the API key
    while True:
        api_key = q.password('Enter your OpenAI API key:\n').ask()
        if auth(api_key, print_success_msg=False):
            break


    # Prompt the user for the organization ID and member name, if desired
    organization_id = q.text('Enter your organization ID (optional):\n').ask().strip()
    member_name = q.text('Enter your member name (optional):\n').ask().strip()
    print()

    # Save the configurations to the file
    config = {
        "api_key": api_key,
        "organization_id": organization_id,
        "member_name": member_name
    }
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=4)
    print(f"Config file saved to {config_file}.")


def load_config(config_dir: str = DEFAULT_CONFIG_DIR) -> Dict[str, str]:
    """
    Load the OpenAI configurations from a JSON file in the specified directory.
    If the directory or file does not exist, ask to create one.
    """
    config_file = os.path.join(config_dir, 'openai_config.json')

    # Check if the file exists
    if not os.path.isfile(config_file):
        print(f"Config file not found at {config_file}!")
        print('Creating...')
        create_or_update_config(config_dir)

    # Load the configurations from the file
    with open(config_file, 'r') as f:
        try:
            config = json.load(f)
        except json.JSONDecodeError:
            print_warning(
                f"Failed to load config file {config_file}: invalid JSON format."
            )
            return None

    print()

    return config
