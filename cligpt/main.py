#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import openai
from typing import Dict, List
from openai.openai_object import OpenAIObject

from colorama import init as colorama_init
from colorama import Fore

from config import create_or_update_config, load_config

MessageList = List[Dict[str, str]]

"""
TODO: 
    - Proxy
    - Interactive mode
    - Saved Conversations
    - Pre-built prompts
"""


def metainitiate():
    """
    Initiate for the first time.
    """
    create_or_update_config()
    # generate_builtin_convs()
    pass


def initiate():
    """
    Function to initiate the CLI application.
    """
    colorama_init(autoreset=True)

    config = load_config()

    if api_env := os.getenv('OPENAI_API_KEY'):
        auth(api_env)
    else:
        auth(config.get('api_key'))

    load_convs()


def auth(api_key: str) -> None:
    """
    Authenticate the API key provided by the user.
    """
    openai.api_key = api_key
    try:
        openai.Model.list()
        print(Fore.GREEN + 'Authenticated!')
    except openai.error.AuthenticationError:
        print(Fore.RED + 'Incorrect API key provided!')


def load_convs():
    pass


def prompt_request(messages: MessageList) -> OpenAIObject:
    response = openai.ChatCompletion.create(model='gpt-3.5-turbo',
                                            messages=messages)
    return response


def retry_request():
    # ['choices'][0]['finish_reason']
    pass

def converse(messages: MessageList=None) -> None:
    user_says = str(input('User: '))
    
    prompt_request(messages).choices


if __name__ == '__main__':
    initiate()

    # msg = [{
    #     "role": "system",
    #     "content": "You are a helpful assistant."
    # }, {
    #     "role": "user",
    #     "content": "Who won the world series in 2020?"
    # }, {
    #     "role": "assistant",
    #     "content": "The Los Angeles Dodgers won the World Series in 2020."
    # }, {
    #     "role": "user",
    #     "content": "Where was it played?"
    # }]
    # rsp = prompt_request(msg)
    # print(type(rsp))
    # print(rsp)
