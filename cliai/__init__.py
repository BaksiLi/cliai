#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TODO:
    - Save Conversations
    - Fast response
        - `cliai ask <message>`
    - Model
        - `cliai audio` with Whisper!
    - Configuration manager
        - `cliai config`
        - set default model, system etc.
    - Preset prompts
        - `cliai git`: Generate Git commit message
    - Provide context
        - `cliai chat -i <file>`
    - Python module (and use in Vim)
"""
__version__ = '0.2.9'
__all__ = ['core', 'config', 'convo', 'cli', 'util']

if __name__ == '__main__':
    for module in __all__:
        exec("import {}".format(module))
    cli.cli()
