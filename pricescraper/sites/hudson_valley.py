#!/usr/bin/env python3
'''This module contains a scraper for SeedLibrary.org'''
import re

from .base import BaseSite


class HudsonValley(BaseSite):
    '''This class scrapes Product data from SeedLibrary.org'''
    ABBREVIATION = 'hv'

    ROOT_URL = 'http://www.seedlibrary.org'
    SEARCH_URL = ROOT_URL + '/catalogsearch/result/?q={}'
    NO_RESULT_TEXT = 'Your search returns no results.'

    def _get_results_from_search_page(self, search_page_html):
        '''Return tuples of names & URLs of search results.'''
        return re.findall(
            r'product-name"><a href=".*?org(.*?)".*?title="(.*?)".*?>',
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
        return 'None Specified'

    def _parse_organic_status_from_product_page(self):
        '''Parse the Product's Organic Status from the Product Page.

        :returns: The Product's Organic Status
        :rtype: :obj:`bool`

        '''
        return 'Certified Organic Seed' in self.page_html

    def _parse_price_from_product_page(self):
        '''Parse the Product's Price from the Product Page.

        :returns: The Product's Price
        :rtype: :obj:`str`

        '''
        return self._get_match_from_product_page(r'span class="price">(.*?)<')

    def _parse_weight_from_product_page(self):
        '''Parse the Product's Weight from the Product Page.

        :returns: The Product's Weight
        :rtype: :obj:`str`

        '''
        return self._get_match_from_product_page(r'class="data">(.*?)<')
