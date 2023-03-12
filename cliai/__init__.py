#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TODO:
    - Save Conversations
    - Improve using rich
    - Improve using prompt_toolkit
    - Preset prompts
    - Proxy
"""
__version__ = '0.2.0'
__all__ = ['core', 'config', 'convo', 'cli', 'util']

if __name__ == '__main__':
    for module in __all__:
        exec("import {}".format(module))
    cli.cli()
