#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ['auth', 'config', 'convo', 'wrapper']
__version__ = 'dev'
__license__ = 'MIT'
__github__ = 'https://github.com/BaksiLi/cligpt'


"""
TODO: 
    - Proxy
    - Save Conversations
    - Pre-built prompts
"""


if __name__ == '__main__':
    for module in __all__:
        exec("import {}".format(module))
    # auth.initiate()
