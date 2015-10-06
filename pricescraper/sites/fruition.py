#!/usr/bin/env python3
'''This module contains a scraper for FruitionSeeds.com'''
import re

from .base import BaseSite


class Fruition(BaseSite):
    '''This class scrapes Product data from FruitionSeeds.com'''
    ABBREVIATION = 'fs'

    ROOT_URL = 'http://www.fruitionseeds.com'
    SEARCH_URL = ROOT_URL + '/SearchResults.asp?Submit=Search&Search={}'
    NO_RESULT_TEXT = 'No products match your search'

    def _get_results_from_search_page(self, search_page_html):
        '''Return tuples of names & URLs of search results.'''
        return re.findall(
            r'href=".*?com(.*?)" class="productname.*?>\s*.*?itemprop=\'name\'>\s*(.*?)\s*<',
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
        return self._get_match_from_product_page(r'ProductCode=(.*?)"')

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
        return self._get_match_from_product_page(r'OPTION.*?>(.*?)\s\[')

    def _parse_weight_from_product_page(self):
        '''Parse the Product's Weight from the Product Page.

        :returns: The Product's Weight
        :rtype: :obj:`str`

        '''
        return self._get_match_from_product_page(r'OPTION.*?\[\s?(.*?)\s?\]')
