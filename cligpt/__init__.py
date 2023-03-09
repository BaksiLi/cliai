#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ['config', 'convo', 'wrapper']
# __version__ = '1.0'
# __license__ = 'MIT'
__github__ = 'https://github.com/BaksiLi/cligpt'

def main():
    for module in __all__:
        exec("import {}".format(module))
