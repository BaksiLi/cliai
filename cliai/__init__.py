#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TODO:
    - Save Conversations
    - Preset prompts
    - Configuration manager
"""
__version__ = '0.2.7'
__all__ = ['core', 'config', 'convo', 'cli', 'util', "preset"]

if __name__ == '__main__':
    for module in __all__:
        exec("import {}".format(module))
    cli.cli()
