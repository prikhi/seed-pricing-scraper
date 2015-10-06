#!/usr/bin/env python3
'''This module contains a scraper for SeedSaversExchange.org'''
import re
import json
import urllib.request

from .base import BaseSite
from util import get_page_html


class SeedSavers(BaseSite):
    '''This class scrapes Product data from SeedSaversExchange.org'''
    ABBREVIATION = 'ss'

    ROOT_URL = 'http://www.seedsavers.org'
    SEARCH_URL = ROOT_URL + '/onlinestore/?search={}'
    NO_RESULT_TEXT = 'No items found.'

    def get_and_set_product_information(self):
        '''Retrieve and set the Product's information from the website

        SeedSavers uses AJAX & Javascript redirects in an attempt to thwart
        bots, so we call ``_get_real_url()`` to generate the real page's URL.
        Incorrect pages do not contain CSS classes ending in ``_cell`` so we
        check for that text to see if we need to find the true page.

        '''
        found_page_text = '_cell'

        self.page_html = self._find_product_page()
        if (self.page_html is not None and
                found_page_text not in self.page_html):
            self.page_html = get_page_html(self._get_real_url())
        self._parse_and_set_attributes()

    def _get_real_url(self):
        '''Generate the true URL of the product by simulating an AJAX request.

        Some product pages linked from search results do not contain data but
        instead use javascript to redirect to a page with the data. The URL to
        redirect to is determined by making an AJAX request to a backend
        script.

        '''
        ajax_path = 'app/site/hosting/scriptlet.nl?script=127&deploy=1&inam='

        item_parent = self._get_match_from_product_page(
            r'itemparent" value="(.*? TOP).*?"').replace(' ', '%20')
        ajax_url = ("{}/{}{}").format(self.ROOT_URL, ajax_path, item_parent)

        request = urllib.request.Request(
            ajax_url, headers={'User-Agent': 'Mozilla/5.0',
                               'Content-Type': 'application/json'})
        response = urllib.request.urlopen(request).read().decode('utf8')
        data = json.loads(response)

        real_path = data['myurl']
        return '{}/{}/'.format(self.ROOT_URL, real_path)

    def _get_results_from_search_page(self, search_page_html):
        '''Return tuples of names & URLs of search results.'''
        return re.findall(r'<h6><a href="(.*?)">(.*?)</a>', search_page_html)

    def _parse_name_from_product_page(self):
        '''Parse the Product's Name from the Product Page.

        :returns: The Product's Name
        :rtype: :obj:`str`

        '''
        return self._get_match_from_product_page(r'<title>(.*?)\s?\|')

    def _parse_number_from_product_page(self):
        '''Parse the Product's Number from the Product Page.

        :returns: The Product's Number
        :rtype: :obj:`str`

        '''
        return self._get_match_from_product_page(r'Catalog <span>(.*?)\s?</')

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
            r'bl_price_cell">\s*(.*?)\s*<')

    def _parse_weight_from_product_page(self):
        '''Parse the Product's Weight from the Product Page.

        :returns: The Product's Weight
        :rtype: :obj:`str`

        '''
        return self._get_match_from_product_page(
            r'bl_description_cell">\s*(.*?)\s*<')
