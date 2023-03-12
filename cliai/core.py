#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from typing import Optional

import openai
import questionary as q

from cliai.config import create_or_update_config, load_config
from cliai.convo import MessageList, load_convo, make_request, save_convo
from cliai.util import (print_not_implemented, print_response, print_success,
                        print_warning, print_role)


def metainitiate():
    """
    Initiate for the first time.
    """
    create_or_update_config()
    # generate_builtin_convs()
    pass


def initiate(api_key: Optional[str] = None):
    """
    Function to initiate the CLI application.
    """
    if api_key:
        auth(api_key)
    elif api_env := os.getenv('OPENAI_API_KEY'):
        auth(api_env)
    else:
        config = load_config()
        auth(config.get('api_key'))

    load_convo()


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


def auth(api_key: str) -> None:
    """
    Authenticate the API key provided by the user.
    """
    openai.api_key = api_key

    if is_authenticated():
        print_success('\tAuthenticated!\n')
    else:
        print_warning('Incorrect API key provided!')


def converse(messages: Optional[MessageList] = None,
             verbose: Optional[bool] = 0) -> None:
    """
    Start chatting.
    """
    if not is_authenticated():
        initiate()

    if messages is None:
        messages = MessageList()

    print('Welcome to chat mode.\n')

    # Ask if to use custom system role
    if not q.confirm('Use the default system role?').ask():
        print_not_implemented()

    # Chat while true
    while True:
        # Ask for user input
        user_says = q.text('', qmark='[User]', multiline=True).ask()
        messages.user_says(user_says)
        print()

        # Make the resquest while true
        while True:
            response = make_request(messages)
            finish_reason = response.choices[0].finish_reason

            if finish_reason == 'stop':
                assistant_says = response.choices[0].message.content

                if verbose:
                    # TODO: Add a counter?
                    print(f'In {response.response_ms}')

                print_role('Assistant')
                print_response(assistant_says)

                user_reaction = q.select('Next', choices=['Continue', 'Retry', 'Quit']).ask()

                if user_reaction == 'Continue':
                    messages.assistant_says(assistant_says)
                    print()
                    break

                # elif user_reaction == 'Modify':

                elif user_reaction == 'Quit':
                    print()
                    if q.confirm('Save this conversation?').ask():
                        save_convo(messages)
                    sys.exit()

            elif finish_reason == 'length':
                q.confirm('Maximum length reached. Retry?').ask()

            print()
