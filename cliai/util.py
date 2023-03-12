#!/usr/bin/env python
# -*- coding: utf-8 -*-

from prompt_toolkit import print_formatted_text as pt_print
from prompt_toolkit.formatted_text import FormattedText as FText
from prompt_toolkit.formatted_text import PygmentsTokens
from prompt_toolkit.styles import Style
from pygments import lex
from pygments.lexer import RegexLexer
from pygments.token import Comment, Generic, Text

# TODO: convert (Enum) to be consistent
STYLE_SHEET = Style([
    ('role', 'fg:#5f819d'),
    ('warning', 'fg:#FF0000'),
    ('success', 'fg:#00FF00'),
    ('pygments.text', ''),  # body
    ('pygments.generic.deleted', 'fg:#808080'),  # disclaimer
    ('pygments.comment.preproc', 'fg:#859900'),  # codes
    ])


class ResponseLexer(RegexLexer):
    tokens = {
        'root': [
            (r'^As\ an\ AI\ language\ model.*?\.', Generic.Deleted),
            (r'[ ^(]`(.*?)`', Comment.Preproc),
            # TODO: Colour based on language
            (r'^```(.*?$\n)?(.*?\n)+?^```$', Comment.Preproc),
            (r'.+?', Text),
        ]
    }


class InputLexer(RegexLexer):
    tokens = {
        'root': [
            (r'[ ^(]`(.*?)`', Comment.Preproc),
            (r'^```(.*?$\n)?(.*?\n)+?^```$', Comment.Preproc),
            (r'.+?', Text),
        ]
    }


def print_response(response: str) -> None:
    tokens = PygmentsTokens(list(lex(response.lstrip(), lexer=ResponseLexer())))
    pt_print(tokens, style=STYLE_SHEET)


def print_role(role: str) -> None:
    # ROLES = ('system', 'assistant', 'user')
    pt_print(FText([('class:role', f'[{role}]')]), style=STYLE_SHEET)


def print_warning(text: str) -> None:
    pt_print(FText([('class:warning', text)]), style=STYLE_SHEET)


def print_success(text: str) -> None:
    pt_print(FText([('class:success', text)]), style=STYLE_SHEET)


def print_not_implemented() -> None:
    print_warning('This function is not available by far!')
