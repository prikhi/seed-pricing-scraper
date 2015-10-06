#!/usr/bin/env python3
'''This module contains a scraper for TerritorialSeed.com'''
import re

from .base import BaseSite


class Territorial(BaseSite):
    '''This class scrapes Product data from TerritorialSeed.com'''
    ABBREVIATION = 'ts'

    ROOT_URL = 'http://www.territorialseed.com'
    SEARCH_URL = ROOT_URL + '/category/s?keyword={}'
    NO_RESULT_TEXT = 'Showing <b>0 - 0</b> out of <b>0</b> total matches'

    def _get_results_from_search_page(self, search_page_html):
        '''Return tuples of names & URLs of search results.'''
        return re.findall(r"product'>\s*<a href='(.*?)'><h2>(.*?)<",
                          search_page_html)

    def _parse_name_from_product_page(self):
        '''Parse the Product's Name from the Product Page.

        :returns: The Product's Name
        :rtype: :obj:`str`

        '''
        return self._get_match_from_product_page(r'<title>(.*?)</title>')

    def _parse_number_from_product_page(self):
        '''Parse the Product's Number from the Product Page.

        :returns: The Product's Number
        :rtype: :obj:`str`

        '''
        return self._get_match_from_product_page(r'child-sku.*?(.*?)</>')

    def _parse_organic_status_from_product_page(self):
        '''Parse the Product's Organic Status from the Product Page.

        :returns: The Product's Organic Status
        :rtype: :obj:`bool`

        '''
        return 'organic' in self.name.lower()

    def _parse_price_from_product_page(self):
        '''Parse the Product's Price from the Product Page.

        :returns: The Product's Price
        :rtype: :obj:`str`

        '''
        return self._get_match_from_product_page(r'child-price.*?(.*?)</>')

    def _parse_weight_from_product_page(self):
        '''Parse the Product's Weight from the Product Page.

        :returns: The Product's Weight
        :rtype: :obj:`str`

        '''
        return self._get_match_from_product_page(r'child-desc.*?(.*?)</>')
