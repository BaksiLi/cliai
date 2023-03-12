#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
from getpass import getpass
from typing import Dict

DEFAULT_CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".cliai")


def create_or_update_config(config_dir: str = DEFAULT_CONFIG_DIR) -> None:
    """
    Create a new OpenAI configuration file in the specified directory.
    If the directory does not exist, it will be created.
    """
    os.makedirs(config_dir, exist_ok=True)
    config_file = os.path.join(config_dir, 'openai_config.json')

    # Prompt the user for the API key
    print()
    while True:
        api_key = getpass("Enter your OpenAI API key:\n").strip()
        if not api_key:
            print("API key cannot be empty.")
        else:
            break

    # Prompt the user for the organization ID and member name, if desired
    organization_id = input(
        "Enter your organization ID (optional):\n").strip() or None
    member_name = input("Enter your member name (optional):\n").strip() or None
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
            print(
                f"Failed to load config file {config_file}: invalid JSON format."
            )
            return None

    print()

    return config
