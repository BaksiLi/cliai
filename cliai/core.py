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
from cliai.util import InputLexer, print_response, print_role, print_warning


def metainitiate():
    """
    Initiate for the first time.
    """
    create_or_update_config()
    # generate_builtin_convs()


def initiate(api_key: Optional[str] = None,
             api_base: Optional[str] = None):
    """
    Function to initiate OpenAI API settings.
    """
    args = {'api_key': [api_key, 'OPENAI_API_KEY']}
            # 'api_base': [api_base, 'OPENAI_API_BASE']}

    if not api_key:
        config = load_config()

    auth_args = {}
    for arg_str in args.keys():
        arg = args[arg_str][0]

        # API Key given as cli arg
        if arg:
            auth_args[arg_str] = arg

        # API Key as shell var (deprecated)
        # elif arg_env := os.getenv(args[arg_str][1]):
        #     auth_args[arg_str] = arg_env

        # API Key from the config
        else:
            auth_args[arg_str] = config.get(arg_str)

    auth(**auth_args)

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

    # Ask which bot to use
    # presets_handler: PresetsHandler = PresetsHandler()
    # preset: Preset = presets_handler.select_preset()

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
            # response = make_request(messages, preset)
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

            elif finish_reason == 'content_filter':
                print_warning('Content flagged by OpenAI!')
                q.confirm('Retry?').ask()

            # null
            else:
                pass

            print()

def manage_config():
    pass

def manage_convos():
    pass
