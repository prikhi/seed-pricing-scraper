#!/usr/bin/env python3
'''This module defines scraping information for BotanicalInterests.com'''

import re

from .base import BaseSite


TITLE_REGEX = r'<title>\s*(.*?) \|'
NUMBER_REGEX = r'<p class="item_num">Item #(\d+)<\/p>'
PRICE_REGEX = r'<h2>\$(\d+\.\d\d).*?<\/h2>'
WEIGHT_REGEX = r'<p>((\d+.\d\d) grams|(\d+) seeds)<\/p>'


class BotanicalInterests(BaseSite):
    '''This class scrapes Product data from BotanicalInterests.com'''
    ABBREVIATION = 'bi'
    ROOT_URL = 'http://www.botanicalinterests.com'
    SEARCH_URL = ROOT_URL + '/products/index/srch:{}/num:high'
    NO_RESULT_TEXT = (
        "Sorry, we couldn’t find any pages that matched your criteria.")

    def _get_results_from_search_page(self, search_page_html):
        '''Parse the Search Page, creating a list of URLs and Product Names

        :param search_page_html: The Search Results Page's HTML
        :type search_page_html: str
        :returns: A list containing each Product's URL and Name
        :rtype: :obj:`list`
        '''
        product_regex = re.compile(
            r'class="list-thumb">\s*?<a href="(.*?)".*?>(.*?)<\/a>'
        )
        return product_regex.findall(search_page_html)

    def _parse_name_from_product_page(self):
        '''Use the Product Page's Title to determine the Variety Name

        :returns: The Product's Name
        :rtype: :obj:`str`
        '''
        return self._get_match_from_product_page(TITLE_REGEX)

    def _parse_number_from_product_page(self):
        '''Parse the Product's Number from the Product Page HTML

        :returns: The Product's Number
        :rtype: :obj:`str`
        '''
        return self._get_match_from_product_page(NUMBER_REGEX)

    def _parse_organic_status_from_product_page(self):
        '''Parse the Product's Organic Status from the Product Page HTML

        This method takes advantage of the fact that BotanicalInterests puts
        ``Organic`` in all their organic product's names.

        :returns: The Product's Organic Status
        :rtype: :obj:`bool`
        '''
        return 'organic' in self.name.lower()

    def _parse_price_from_product_page(self):
        '''Parse the Product's Price from the Product Page HTML

        :returns: The Product's Price
        :rtype: :obj:`str`
        '''
        return self._get_match_from_product_page(PRICE_REGEX)

    def _parse_weight_from_product_page(self):
        '''Parse the Product's Weight from the Product Page HTML

        The returned weight may be in grams or number of seeds, depending on
        which BotanicalInterests chooses to display for the product.

        :returns: The Product's Weight
        :rtype: :obj:`str`
        '''
        return self._get_match_from_product_page(WEIGHT_REGEX)
