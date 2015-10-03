#!/usr/bin/env python3
'''This module contains a scraper for JohnnySeeds.com'''
import re

from .base import BaseSite
from util import remove_punctuation


class JohnnySeeds(BaseSite):
    '''This class scrapes Product data from JohnnySeeds.com'''
    ABBREVIATION = 'js'

    ROOT_URL = 'http://www.johnnyseeds.com'
    SEARCH_URL = ROOT_URL + '/search.aspx?searchterm={}'
    NO_RESULT_TEXT = 'Sorry — we did not find any items matching your search.'

    def _get_results_from_search_page(self, search_page_html):
        '''Return tuples of names & URLs of search results.'''
        matches = re.findall(
            r'<div class="container"><a href=".*?com(.*?)"class="productAnchor"\s*><span class="nameCAT">(.*?)</span><span.*?extendednameCAT">(.*?)<',
            search_page_html)

        groups = []
        for link, name, extra_name in matches:
            groups.append((link, '{} {}'.format(name, extra_name)))
        return groups

    def _parse_name_from_product_page(self):
        '''Parse the Product's Name from the Product Page HTML

        :returns: The Product's Name
        :rtype: :obj:`str`

        '''
        return self._get_match_from_product_page(r'<title>\s*(.*?) -')

    def _parse_number_from_product_page(self):
        '''Parse the Product's Number from the Product Page HTML

        :returns: The Product's Number
        :rtype: :obj:`str`

        '''
        return self._get_match_from_product_page(
            r'<p id="SKUField".*?>(.*?)</p>')

    def _parse_organic_status_from_product_page(self):
        '''Parse the Product's Organic Status from the Product Page HTM

        :returns: The Product's Organic Status
        :rtype: :obj:`bool`

        '''
        return ('<img border="0" title="Organic Seeds, Plants, and Supplies" alt="Organic Seeds, Plants, and Supplies" src="skins/Skin_1/CustomImages/105466040932518.gif">'
                in self.page_html)

    def _parse_price_from_product_page(self):
        '''Parse the Product's Price from the Product Page HTM

        :returns: The Product's Price
        :rtype: :obj:`str`

        '''
        return self._get_match_from_product_page(
            r'variantprice">\s*(.*?)</span')

    def _parse_weight_from_product_page(self):
        '''Parse the Product's Weight from the Product Page HTM

        :returns: The Product's Weight
        :rtype: :obj:`str`

        '''
        packet_count = self._get_match_from_product_page(
            r'Packet:\s*(\d+ seeds)')
        return (packet_count if packet_count is not None else
                self._get_match_from_product_page(r'ItemName\d+">(.*?)</span'))
