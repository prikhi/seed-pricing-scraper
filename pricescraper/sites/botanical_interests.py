#!/usr/bin/env python3
#import re
import urllib

from .base import BaseSite


class BotanicalInterests(BaseSite):
    '''This class scrapes Product data from BotanicalInterests.com'''
    _COMPANY_ABBREVIATION = 'bi'

    _ROOT_URL = 'http://www.botanicalinterests.com'
    _SEARCH_URL = 'http://www.botanicalinterests.com/products/index/srch:'
    _NO_RESULT_TEXT = ("Sorry, we couldn&rsquo;t find any pages that matched "
                       "your criteria.")

    def _find_product_page(self):
        '''Find the best matching Product and return the Product Page's HTML

        This method will first search the site using only SESE's Product Name.
        If no result if found, it will try to use the Product Name and
        Category.

        BotanicalInterests include ``Organic`` in the Product Names of their
        Varieties, so if the SESE variety is organic, ``Organic`` will be added
        to the search terms.

        If no Product is found using the Name and Category, the method will
        return None instead of any HTML.

        :returns: The Product Page's HTML or :obj:`None`
        :rtype: string
        '''
        if self.sese_organic:
            search_term = self.sese_name + " Organic"
        else:
            search_term = self.sese_name
        name_search = self._search_site(search_term)
        matching_page = self._get_best_match_or_none(name_search)

        if matching_page is None:
            category_search = self._search_site(search_term + " " +
                                                self.sese_category)
            matching_page = self._get_best_match_or_none(category_search)

        return matching_page

    def _search_site(self, search_terms):
        '''Search the BotanicalInterests website for ``search_terms``

        :param search_terms: The keywords to search for
        :type search_terms: string
        :returns: The Search Result Page's HTML
        :rtype: string
        '''
        encoded_keywords = urllib.parse.quote(search_terms)
        search_url = self._SEARCH_URL + encoded_keywords
        request = urllib.request.Request(search_url, headers={'User-Agent':
                                                              'Mozilla/5.0'})
        result_page = str(urllib.request.urlopen(request).read())
        return result_page

    def _get_best_match_or_none(self, search_page_html):
        '''Attempt to find the best match on the Search Results HTML

        If no results are found, the method will return :obj:`None`.

        :param search_page_html: The Search Results Page's HTML
        :type search_page_html: string
        :returns: Product Page HTML of the best match or None if no good match
        :rtype: string or :obj:`None`
        '''
        if self._NO_RESULT_TEXT in search_page_html:
            return None

    def _parse_name_from_product_page(self):
        '''Use the Product Page's Title to determine the Variety Name

        :returns: The Product's Name
        :rtype: :obj:`str`
        '''

    def _parse_number_from_product_page(self):
        '''Parse the Product's Number from the Product Page HTML

        :returns: The Product's Number
        :rtype: :obj:`str`
        '''

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

    def _parse_weight_from_product_page(self):
        '''Parse the Product's Weight from the Product Page HTML

        The returned weight may be in grams or number of seeds, depending on
        which BotanicalInterests chooses to display for the product.

        :returns: The Product's Weight
        :rtype: :obj:`str`
        '''
