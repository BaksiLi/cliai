#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from typing import Optional

import openai
from colorama import Fore
from colorama import init as colorama_init

from cliai.config import create_or_update_config, load_config
from cliai.convo import (MessageList, load_convo, make_request, retry_request,
                         save_convo, stylize_response)


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
    colorama_init(autoreset=True)

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
        print(Fore.GREEN + '\nAuthenticated!\n')
    else:
        print(Fore.RED + 'Incorrect API key provided!')


def converse(messages: Optional[MessageList] = None,
             verbose: Optional[bool] = 0) -> None:
    if not is_authenticated():
        initiate()

    if messages is None:
        messages = MessageList()

    # TODO: ask for system
    pass

    try:
        # TODO: Add a counter?
        print('Welcome to chat mode.\nType to chat, double press <Enter> to send, <Ctrl-C> to quit.\n')
        while True:
            # Ask for user input
            print('User: ')
            user_says = ''
            while True:
                user_says += input('\t') + '\n'
                if user_says[-2:] == '\n\n':
                    break
            messages.user_says(user_says)

            response = make_request(messages)
            finish_reason = response.choices[0].finish_reason 
            if finish_reason == 'stop':
                assistant_says = response.choices[0].message.content
                if verbose:
                    print(
                        f'Assistant (in {response.response_ms}): {stylize_response(assistant_says)}'
                    )
                else:
                    print(f'Assistant:\n\t{stylize_response(assistant_says)}')
                messages.assistant_says(assistant_says)
            elif finish_reason == 'length':
                print(Fore.YELLOW + 'Maximum length reached.')
            else:
                retry_request()

            print()

    except KeyboardInterrupt:
        if_save = bool(input(Fore.YELLOW +
                             '\nSave this conversation? (y/N): '))
        if if_save:
            save_convo(messages)
        sys.exit()
