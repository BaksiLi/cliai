#!/usr/bin/env python
# -*- coding: utf-8 -*-

from colorama import Fore


def stylize_response(response: str):
    """
    Stylize the response.
    May be replaced by a prompt-lexer.
    """
    indent = ''
    return response.lstrip().replace('\n', '\n' + indent)


def print_not_implemented():
    print(Fore.RED + 'This function is not available by far!')
