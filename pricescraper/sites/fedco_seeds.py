#!/usr/bin/env python3
'''This module contains a scraper for FedcoSeeds.com'''
import re

from .base import BaseSite
from util import remove_punctuation


class FedcoSeeds(BaseSite):
    '''This class scrapes Product data from FedcoSeeds.com'''
    ABBREVIATION = 'fs'

    ROOT_URL = 'http://www.fedcoseeds.com'
    SEARCH_URL = ROOT_URL + '/seeds/search?search={}'

    def _find_product_page(self, use_organic=True):
        '''Find the Product Page from the Company's website.

        If there was only one result, the site will redirect to it's product
        page. We check for this by looking for the text ``Back to Search
        Results`` in the search results page.

        :param use_organic: Whether or not to check for a non-organic version
                            of the product.
        :type use_organic: bool
        :returns: The Product Page's HTML or :obj:`None`
        :rtype: :obj:`str`

        '''
        search_terms = remove_punctuation(self.sese_name)
        if use_organic and self.sese_organic:
            search_terms += " organic"
        search_page = self._search_site(search_terms)

        was_redirected_to_product = 'Back to Search Results' in search_page
        if was_redirected_to_product:
            return search_page

        match = self._get_best_match_or_none(search_page)
        check_without_organic = (
            self.sese_organic and match is None and use_organic)
        return (match if not check_without_organic else
                self._find_product_page(use_organic=False))

    def _get_results_from_search_page(self, search_page_html):
        '''Return tuples of names & URLs of search results.'''
        return re.findall(
            r'href="(.*?)".*?class="name".*?>(?:<span class="subcategory">)?(.*?)(?:</span>|</a>)',
            search_page_html)

    def _parse_name_from_product_page(self):
        '''Parse the Product's Name from the Product Page HTML

        :returns: The Product's Name
        :rtype: :obj:`str`

        '''
        return self._get_match_from_product_page(r'Item: (.*?)</title>')

    def _parse_number_from_product_page(self):
        '''Parse the Product's Number from the Product Page HTML

        :returns: The Product's Number
        :rtype: :obj:`str`

        '''
        return self._get_match_from_product_page(
            r'<div align="justify">\s+<strong>\s+(.*?)\s.*?<')

    def _parse_organic_status_from_product_page(self):
        '''Parse the Product's Organic Status from the Product Page HTM

        :returns: The Product's Organic Status
        :rtype: :obj:`bool`

        '''
        return ('<span class="og-eco" title="Certified Organic">OG</span>'
                in self.page_html)

    def _parse_price_from_product_page(self):
        '''Parse the Product's Price from the Product Page HTM

        :returns: The Product's Price
        :rtype: :obj:`str`

        '''
        return self._get_match_from_product_page(r'A=\S+ for (\$\d*\.?\d*)')

    def _parse_weight_from_product_page(self):
        '''Parse the Product's Weight from the Product Page HTM

        :returns: The Product's Weight
        :rtype: :obj:`str`

        '''
        return self._get_match_from_product_page(r'A=(\S+).*?<')
