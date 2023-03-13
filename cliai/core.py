#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from typing import Optional

import questionary as q
from prompt_toolkit.lexers import PygmentsLexer

from cliai.config import (auth, create_or_update_config, is_authenticated,
                          load_config)
from cliai.convo import MessageList, load_convo, make_request, save_convo
from cliai.util import InputLexer, print_role, print_response


def metainitiate():
    """
    Initiate for the first time.
    """
    create_or_update_config()
    # generate_builtin_convs()


def initiate(api_key: Optional[str] = None):
    """
    Function to initiate the CLI application.
    """
    # API Key given as cli arg
    if api_key:
        auth(api_key)
    # API Key as shell var
    elif api_env := os.getenv('OPENAI_API_KEY'):
        auth(api_env)
    # API Key from the config
    else:
        config = load_config()
        auth(config.get('api_key'))

    load_convo()


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
        print()
        print_role('System')
        messages.update_system(q.text('', qmark='', lexer=PygmentsLexer(InputLexer)).ask().strip())
        print()

    # Chat while true
    while True:
        # Ask for user input
        print_role('User')
        user_says = q.text('', qmark='', multiline=True, lexer=PygmentsLexer(InputLexer)).ask()
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

                user_reaction = q.select('Next', 
                                         choices=['Continue', 'Modify', 'Retry', 'Quit']
                                         ).ask()

                if user_reaction == 'Continue':
                    messages.assistant_says(assistant_says)
                    print()
                    break

                elif user_reaction == 'Modify':
                    modify_choice = q.select('Which of the following do you want to modify?',
                                             choices = ['User', 'Assistant', 'System']
                                             ).ask()

                    if modify_choice == 'User':
                        messages.recall_last()
                        print()
                        break
                    elif modify_choice == 'Assistant':
                        messages.recall_last()
                        print()
                        print_role('Assistant')
                        assistant_says = q.text('', qmark='', multiline=True, lexer=PygmentsLexer(InputLexer)).ask()
                        messages.assistant_says(assistant_says)
                        print()
                        break
                    elif modify_choice == 'System':
                        print_role('System')
                        messages.update_system(q.text('', qmark='', lexer=PygmentsLexer(InputLexer)).ask().strip())
                        print()

                elif user_reaction == 'Retry':
                    pass

                elif user_reaction == 'Quit':
                    print()
                    if q.confirm('Save this conversation?').ask():
                        save_convo(messages)
                    sys.exit()

            elif finish_reason == 'length':
                q.confirm('Maximum length reached. Retry?').ask()

            print()
