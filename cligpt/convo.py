#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Dict, List

import openai
from colorama import Fore
from openai.openai_object import OpenAIObject


class MessageList(List[Dict[str, str]]):

    def __init__(self):
        super().__init__()

    def __repr__(self):
        return f"MessageList({super().__repr__()})"

    def __str__(self):
        return self.__repr__()

    def append(self, item: Dict[str, str]):
        if not isinstance(item, dict):
            raise TypeError("Item must be a dictionary.")
        super().append(item)

    def user_says(self, content: str):
        super().append({'role': 'user', 'content': f'{content}'})

    def assistant_says(self, content: str):
        super().append({'role': 'assistant', 'content': f'{content}'})

    def update_system(self, content: str):
        pass

    def extend(self, items: List[Dict[str, str]]):
        if not all(isinstance(item, dict) for item in items):
            raise TypeError("Items must be a list of dictionaries.")
        super().extend(items)


def make_request(messages: MessageList) -> OpenAIObject:
    response = openai.ChatCompletion.create(model='gpt-3.5-turbo',
                                            messages=messages)
    return response


def retry_request():
    # ['choices'][0]['finish_reason']
    # response.response_ms
    pass


def stylize_response(response: str):
    indent = '\t'
    return response.lstrip().replace('\n', '\n' + indent)


def save_convo(messages: MessageList) -> None:
    print(Fore.RED + 'This function is not available by far!')
    pass


def load_convo():
    # print(Fore.RED + 'This function is not available by far!')
    pass
