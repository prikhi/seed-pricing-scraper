#!/usr/bin/env python3
'''This module provides utility functions for the application'''

import html.parser
import string
import urllib.request

import settings


def get_class(class_string):
    '''Return the Class object of the specified string'''
    parts = class_string.split('.')
    module_string = ".".join(parts[:-1])
    module = __import__(module_string)
    for comp in parts[1:]:
        module = getattr(module, comp)
    return module


def get_page_html(page_url):
    '''Visit the ``page_url`` and return the HTML of the page.

    :param page_url: The URL of the page to grab
    :type page_url: str
    :returns: The HTML of the page
    :rtype: :obj:`str`
    '''
    parser = html.parser.HTMLParser()
    request = urllib.request.Request(page_url, headers={'User-Agent':
                                                        'Mozilla/5.0'})
    page_html = urllib.request.urlopen(request).read()
    try:
        page_html = page_html.decode('iso-8859-1')
    except UnicodeEncodeError:
        pass
    unescaped_html = parser.unescape(page_html)
    return unescaped_html


def remove_punctuation(text):
    '''Remove all Punctuation marks from the supplied string

    :returns: The String with no punctuation
    :rtype: :obj:`str`
    '''
    remove_punctuation_map = dict((ord(char), None) for char in
                                  string.punctuation)
    return text.translate(remove_punctuation_map)


def create_header_list():
    '''Generate a list of Header strings for data export

    :returns: Ordered list of Header Name strings
    :rtype: :obj:`list`
    '''
    header_list = []
    for sese_header in settings.SESE_HEADER_ORDER:
        header_list.append(settings.ATTRIBUTES_TO_NAMES[sese_header])
    for company in settings.COMPANY_HEADER_ORDER:
        company_abbrev = company.upper()
        for attribute in settings.ATTRIBUTE_HEADER_ORDER:
            attribute_name = settings.ATTRIBUTES_TO_NAMES[attribute]
            header_name = " ".join([company_abbrev, attribute_name])
            header_list.append(header_name)
    return header_list
