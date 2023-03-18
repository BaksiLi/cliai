#!/usr/bin/env python # -*- coding: utf-8 -*-

from enum import Enum
from typing import Dict, List

import openai
from openai.openai_object import OpenAIObject

from cliai.util import print_not_implemented


class ChatCompletionsModel(str, Enum):
    """
    https://platform.openai.com/docs/models/model-endpoint-compatibility
    """
    ENDPOINT = '/v1/chat/completions'
    GPT_3_5_turbo = 'gpt-3.5-turbo'
    GPT_3_5_turbo_0301 = 'gpt-3.5-turbo-0301'
    GPT_4 = 'gpt-4'
    GPT_4_0314 = 'gpt-4-0314'
    GPT_4_32K = 'gpt-4-32k'
    GPT_4_32K_0314 = 'gpt-4-32k-0314'


class MessageList(List[Dict[str, str]]):
    def __init__(self):
        super().__init__()
        if not self.__len__():
            self.update_system('You are an assistant who answers every question the user asks')

    def __repr__(self):
        return f"MessageList({super().__repr__()})"

    def __str__(self):
        return self.__repr__()

    def append(self, item: Dict[str, str]):
        if not isinstance(item, dict):
            raise TypeError("Item must be a dictionary.")
        super().append(item)

    def update_system(self, content: str):
        """
        Only the latest system prompt will be effective (experiment result).
        """
        # remove all messages with "role": "system"
        self[:] = [msg for msg in self if msg.get("role") != "system"]

        # append the new
        self.append({"role": "system", "content": content})

    def user_says(self, content: str):
        super().append({"role": "user", "content": f"{content}"})

    def assistant_says(self, content: str):
        super().append({"role": "assistant", "content": f"{content}"})

    def recall_last(self):
        super().pop()


class Parameters:
    """
    The parameter object for ChatCompletions.
    It includes parts of the API settings, plus the system_role.
    """
    def __init__(self,
                 model: ChatCompletionsModel = ChatCompletionsModel.GPT_3_5_turbo,
                 start_up_prompts: MessageList = None,
                 temperature: float = None,
                 top_p: float = None,
                 max_tokens: int = None,
                 freq_penalty: float = None,
                 pres_penalty: float = None
                 ):
        self.model = model
        self.start_up_prompts = start_up_prompts

        self.temperature = temperature
        self.top_p = top_p

        self.max_tokens = max_tokens
        self.freq_penalty = freq_penalty
        self.pres_penalty = pres_penalty

        # Not sure if other settings work
        # self.logit_bias: Dict =

    def save(self, path: str):
        pass

    def load(self, path: str):
        pass



class Conversation:
    """
    A conversation includes message history, partial params, and a few metadata.

    https://platform.openai.com/docs/api-reference/chat/create
    """

    def __init__(self, 
                 params: Parameters = Parameters(),
                 messages: MessageList = MessageList(),
                 convo_title: str = None,
                 num_choices: int = 1,
                 ):
        if convo_title:
            self.convo_title = convo_title
        else:
            convo_title = 'Untitled'
            # TODO: If messages is not empty, ask model for the title

        # Metadata (retrieve from response)
        # self.convo_id = convo_id
        # self.created = created
        # self.user: Optional[str] = hash(user)

        # Pre-settings
        self.num_choices: int = 1
        self.params = params

        if params.start_up_prompts:
            self.messages = params.start_up_prompts + messages
        else:
            self.messages = messages


    def show(self):
        # only show head and the end of the conversation
        pass

    def save(self, path: str):
        """
        Export the conversation to a file.
        """
        pass

    def save_params(self, path: str):
        pass

    def load_params(self, path: str, overwrite: bool=True):
        pass

    def make_request(self, stream: bool = False) -> OpenAIObject:
        # TODO: check if self.params.xxx
        response = openai.ChatCompletions.create(
            model=self.params.model,
            messages=self.messages,
            n=self.num_choices,
            temperature=self.params.temperature,
            top_p=self.params.top_p,
            max_tokens=self.params.max_tokens,
            stream=stream
        )
        return response


def make_request(messages: MessageList) -> OpenAIObject:
    response = openai.ChatCompletions.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    return response


def save_convo(messages: MessageList) -> None:
    print_not_implemented()
    pass


def load_convo():
    # print(fore.red + 'this function is not available by far!')
    pass
