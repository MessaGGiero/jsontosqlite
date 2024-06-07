#!/usr/bin/env python
"""
    Flex Cosmos data management
    __author__ = "Massimo Iannuzzi"
    __copyright__ = "free use"
    __license__ = "MIT License"
    __maintainer__ = "Massimo Iannuzzi"
    __email__ = "max.iannuzzi@gmail.com"
"""
def collapse(sg,layout,is_visible, key):
    """
    Helper function that creates a Column that can be later made hidden, thus appearing "collapsed"
    :param layout: The layout for the section
    :param key: Key used to make this seciton visible / invisible
    :return: A pinned column that can be placed directly into your layout
    :rtype: sg.pin
    """
    return sg.pin(sg.Column(layout, key=key,visible=is_visible))