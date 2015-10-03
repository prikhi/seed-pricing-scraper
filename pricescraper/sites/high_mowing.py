#!/usr/bin/env python3
'''This module contains a scraper for HighMowingSeeds.com'''
import re

from .base import BaseSite


class HighMowing(BaseSite):
    '''This class scrapes Product data from HighMowingSeeds.com'''
    ABBREVIATION = 'hm'

    ROOT_URL = 'http://www.highmowingseeds.com'
    SEARCH_URL = ROOT_URL + '/_search.php?q={}'
    NO_RESULT_TEXT = '0 Results found for'
    INCLUDE_CATEGORY_IN_SEARCH = True

    def _get_results_from_search_page(self, search_page_html):
        '''Return tuples of names & URLs of search results.'''
        return re.findall(
            r'<a.*?href="(.*?)">\s*<font class="ProductTitle">\s*(.*?)\s*</font>',
            search_page_html)

    def _parse_name_from_product_page(self):
        '''Parse the Product's Name from the Product Page.

        :returns: The Product's Name
        :rtype: :obj:`str`

        '''
        return self._get_match_from_product_page(
            r'<td class="prod_desc">\s*<span><span.*?bold.*?>(.*?)</span>')

    def _parse_number_from_product_page(self):
        '''Parse the Product's Number from the Product Page.

        :returns: The Product's Number
        :rtype: :obj:`str`

        '''
        return self._get_match_from_product_page(
            r'<tr class="chart_dark">\s*<td>(.*?)</td>')

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
        return self._get_match_from_product_page(
            r'class="chart_dark">\s*(?:<td>.*?</td>\s*){3}<td>\s*(.*?)\s*</td>')

    def _parse_weight_from_product_page(self):
        '''Parse the Product's Weight from the Product Page.

        :returns: The Product's Weight
        :rtype: :obj:`str`

        '''
        return self._get_match_from_product_page(
            r'class="chart_dark">\s*<td>.*?</td>\s*<td>\s*(.*?)\s*</td>')
