#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from textwrap import dedent
from time import time
from typing import Optional

import questionary as q
from prompt_toolkit.lexers import PygmentsLexer

from cliai.config import (DEFAULT_CONFIG_DIR, auth, create_or_update_config,
                          is_authenticated, load_config)
from cliai.convo import Conversation, MessageList
from cliai.util import (InputLexer, print_response, print_role, print_verbose,
                        print_warning)


def metainitiate():
    """
    Initiate for the first time.
    """
    # generate_builtin_convs()
    pass


def initiate(api_key: Optional[str] = None,
             api_base: Optional[str] = None,
             verbose: Optional[bool] = False):
    """
    Function to initiate OpenAI API settings.
    """
    args = {'api_key': [api_key, 'OPENAI_API_KEY'],
            'api_base': [api_base, 'OPENAI_API_BASE']}

    # If no API key is given as arg
    # this will start the create process
    if not api_key:
        config = load_config()
        print_verbose('Config loaded from config file.', verbose)

    auth_args = {}
    for arg_str in args.keys():
        arg = args[arg_str][0]

        # Arg given as cli arg
        if arg:
            auth_args[arg_str] = arg
            if verbose:
                print_verbose(f'{arg_str} loaded from argument as {arg}.', verbose)

        # Arg from the config
        else:
            auth_args[arg_str] = config.get(arg_str)
            if verbose:
                print_verbose(f'{arg_str} loaded from config file as {arg}.', verbose)

    auth(**auth_args, verbose=verbose)

    # load_presets()


def converse(message: Optional[MessageList] = None,
             stream: Optional[bool] = False,
             verbose: Optional[bool] = False) -> None:
    """
    Start chatting.
    """
    if not is_authenticated():
        initiate(verbose=verbose)

    print('Welcome to Chat Mode.\n')

    if stream:
        print_warning('You are using stream mode. Syntax highlighting is not supported!')

    # Ask which bot to use
    # presets_handler: PresetsHandler = PresetsHandler()
    # preset: Preset = presets_handler.select_preset()

    messages = MessageList()

    # TODO: ignore input
    # Provide the message from arg
    if message:
        messages.user_says(content=message)

    conversation = Conversation(messages=messages)

    # TODO: re-consider this

    # Ask if to use custom system role
    if not q.confirm('Use the default system role?').ask():
        print()
        print_role('System')
        system_prompt = q.text('', 
                               qmark='',
                               lexer=PygmentsLexer(InputLexer)).ask()

        if system_prompt:
            conversation.update_system(system_prompt.strip())

    print()

    # Chat while true
    while True:
        # Ask for user input
        print_role('User')
        user_says = q.text('', qmark='',
                           multiline=True,
                           lexer=PygmentsLexer(InputLexer)).ask()
        conversation.user_says(user_says)
        print()

        # Make the resquest while true
        while True:
            print_role('Assistant')

            if not stream:
                if response := conversation.receive_response():
                    assistant_says = response.choices[0].message.content
                    print_response(assistant_says)
                    response_time = response.response_ms
            else:
                assistant_says = ''
                start_time = time()

                response = conversation.receive_stream_response()

                for chunk in response:
                    delta = chunk.choices[0].get('delta')

                    # it could be None or 'assistant'
                    if delta_content := delta.get('content'):
                        print(delta_content, end='')
                        assistant_says += delta_content

                response_time = time() - start_time

            # If verbose, print message
            print_verbose(dedent(f'''
                          Prompt #{conversation.messages.__len__()}
                          Response in {response_time} ms
                          '''), verbose)

            print()

            user_reaction = q.select('Next', choices=['Continue', 'Modify', 'Retry', 'Quit']).ask()

            if user_reaction == 'Continue':
                conversation.assistant_says(assistant_says)
                print()
                break

            elif user_reaction == 'Modify':
                modify_choice = q.select('Which of the following do you want to modify?',
                                         choices = ['User', 'Assistant', 'System']
                                         ).ask()

                if modify_choice == 'User':
                    conversation.messages.recall_last()
                    print()
                    break
                elif modify_choice == 'Assistant':
                    conversation.messages.recall_last()
                    print()
                    print_role('Assistant')
                    assistant_says = q.text('', qmark='', multiline=True, lexer=PygmentsLexer(InputLexer)).ask()
                    conversation.assistant_says(assistant_says)
                    print()
                    break
                elif modify_choice == 'System':
                    print_role('System')
                    conversation.update_system(q.text('', qmark='', lexer=PygmentsLexer(InputLexer)).ask().strip())
                    print()
                    break

            elif user_reaction == 'Retry':
                pass

            elif user_reaction == 'Quit':
                print()
                if q.confirm('Save this conversation?').ask():
                    # conversation.save(path=)
                    pass
                sys.exit()

            print()

def manage_config():
    pass

def manage_convos():
    pass
