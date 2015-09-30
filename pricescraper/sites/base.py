#!/usr/bin/env python3
'''This module defines the Abstract Class all new Websites should sub-class'''
from abc import abstractmethod, ABCMeta
import re
import urllib.parse

import settings
from util import remove_punctuation, get_page_html


class BaseSite(object):
    '''The BaseSite class is an Abstract class for creating new Site classes.

    For each website that needs to be scraped, a Class should be created,
    inheriting and implementing this Abstract Base class.

    The product page searching and parsing methods must be implemented by any
    of this Classes children.

    The ABBREVIATION class attribute must be set & unique for all Sites. The
    SEARCH_URL attribute must be set if the _search_site method is called.

    '''
    __metaclass__ = ABCMeta

    #: The root URL of the Site, no trailing slash necessary
    ROOT_URL = None

    #: The URL for searching the Site, with a pair of braces for inserting the
    #  query using the .format() method. For example,
    #  ``"http://mysite.com?q={}"``.
    SEARCH_URL = None

    #: Unique text present on the Site when there are no search results,
    #  setting this is optional.
    NO_RESULT_TEXT = None

    def __init__(self, name, category, organic):
        '''The Constructor sets the supplied variables as SESE's attributes.

        :param name: SESE's name for this Product
        :type name: str
        :param category: SESE's category for this Product
        :type category: str
        :param organic: SESE's organic status for this Product
        :returns: :obj:`None`
        '''
        self.sese_name = name
        self.sese_category = category
        self.sese_organic = organic
        self.name = self.number = self.organic = None
        self.price = self.weight = self.page_html = None

    def get_company_attributes(self):
        '''Return a dictionary containing this Company's Product attributes '''
        return {'name': self.name,
                'number': self.number,
                'organic': self.organic,
                'price': self.price,
                'weight': self.weight}

    def get_and_set_product_information(self):
        '''Retrieve and set the Product's information from the website'''
        self.page_html = self._find_product_page()
        self._parse_and_set_attributes()

    @abstractmethod
    def _find_product_page(self):
        '''Find the Product Page from the Company's website.

        :returns: The Product Page's HTML or :obj:`None`
        :rtype: :obj:`str`
        '''

    def _parse_and_set_attributes(self):
        '''Parse the Product Page to find and set the Products's attributes

        If no good match was found(and therefore ``self.page_html`` is
        :obj:`None`) the Product's name will be set to "Not Found" and all
        other attributes will be set to :obj:`None`.
        '''
        if self.page_html is None:
            self.name = "Not Found"
            self.number = self.organic = self.price = self.weight = None
            return
        self.name = self._parse_name_from_product_page()
        self.number = self._parse_number_from_product_page()
        self.organic = self._parse_organic_status_from_product_page()
        self.price = self._parse_price_from_product_page()
        self.weight = self._parse_weight_from_product_page()

    def _search_site(self, search_terms):
        '''Return the HTML from searching SEARCH_URL using ``search_terms``.

        Requires the class to have a SEARCH_URL attribute.

        :param search_terms: The keywords to search for
        :type search_terms: str
        :returns: The Search Result Page's HTML
        :rtype: :obj:`str`
        '''
        assert self.SEARCH_URL is not None
        escaped_keywords = urllib.parse.quote(search_terms)
        search_url = self.SEARCH_URL.format(escaped_keywords)
        return get_page_html(search_url)

    def _get_best_match_or_none(self, search_page_html):
        '''Attempt to find the best match on the Search Results HTML.

        The method will first attempt to find a Product that contains the name
        of the SESE variety. Otherwise it will use the Product with the most
        words in common with the SESE variety name, if a minimum percentage of
        the words match(specified by
        :data:`settings.MINIMUM_NAME_MATCHING_PERCENTAGE`).

        If no results are found, the method will return :obj:`None`.

        :param search_page_html: The Search Results Page's HTML
        :type search_page_html: str
        :returns: Product Page HTML of the best match or :obj:`None` if no good
                  match is found
        :rtype: :obj:`str`
        '''
        products = self._get_results_from_search_page(search_page_html)
        has_no_results = len(products) == 0 or (
            self.NO_RESULT_TEXT is not None and
            self.NO_RESULT_TEXT in search_page_html
        )
        if has_no_results:
            return None

        for product in products:
            relative_url, product_name = product
            clean_product_name = remove_punctuation(product_name).lower()
            clean_sese_name = remove_punctuation(self.sese_name).lower()
            if clean_sese_name in clean_product_name:
                page_url = self.ROOT_URL + relative_url
                return get_page_html(page_url)

        product_ranks = self._prepend_name_match_amounts(products)
        best_match = product_ranks[0]
        match_amount = best_match[0]
        if match_amount >= settings.MINIMUM_NAME_MATCHING_PERCENTAGE:
            match_url = self.ROOT_URL + best_match[1][0]
            return get_page_html(match_url)

    @abstractmethod
    def _get_results_from_search_page(self, search_page_html):
        '''Parse the Search Page, creating a list of URLs and Product Names

        :param search_page_html: The Search Results Page's HTML
        :type search_page_html: str
        :returns: A list containing each Product's URL and Name
        :rtype: :obj:`list`
        '''

    def _prepend_name_match_amounts(self, search_results):
        '''Prepend the % of SESE Name matched to the ``search_results`` list.

        ``search_results`` should be a list of (URL, Name) tuples.

        This method iterates through the provided ``search_results`` comparing
        the Product Name with the SESE Product Name by calculating the
        percentage of words in the Company's Name that are also in the SESE
        Name.

        The match percentage will be prepended to each :obj:`tuple` in the
        ``search_results`` returning a list of ``[(Match Percentage, (URL,
        Name)),...]``

        :param search_results: A list of tuples containing the ``(URL, Name)``
                               of each matching Product
        :type search_results: list
        :returns: A list of tupes containing ``(Match%, (URL, Name))`` of each
                  Product
        :rtype: :obj:`list`

        '''
        sese_words = [remove_punctuation(x) for x in
                      self.sese_name.lower().split() +
                      self.sese_category.lower().split()]
        number_of_sese_words = len(sese_words)
        output = []
        for result in search_results:
            number_of_matches = 0
            site_words = [remove_punctuation(x) for x in
                          result[1].lower().split()]
            number_of_site_words = len(site_words)

            for word in site_words:
                if word in sese_words:
                    number_of_matches += 1

            percent_site_words_matched = (
                float(number_of_matches) / number_of_site_words * 100)
            site_to_sese_word_ratio = (
                float(number_of_site_words) / number_of_sese_words)
            percent_sese_words_matched = min(
                float(number_of_matches) / number_of_sese_words * 100, 100)
            sese_to_site_word_ratio = (
                float(number_of_sese_words) / number_of_site_words)

            match_percentage = (
                percent_site_words_matched * site_to_sese_word_ratio +
                percent_sese_words_matched * sese_to_site_word_ratio
            ) / 2
            output.append((match_percentage, result))
        output.sort(key=lambda x: x[0], reverse=True)
        return output

    @abstractmethod
    def _parse_name_from_product_page(self):
        '''Parse the Product's Name from the Product Page HTML

        :returns: The Product's Name
        :rtype: :obj:`str`
        '''

    @abstractmethod
    def _parse_number_from_product_page(self):
        '''Parse the Product's Number from the Product Page HTML

        :returns: The Product's Number
        :rtype: :obj:`str`
        '''

    @abstractmethod
    def _parse_organic_status_from_product_page(self):
        '''Parse the Product's Organic Status from the Product Page HTM

        :returns: The Product's Organic Status
        :rtype: :obj:`bool`
        '''

    @abstractmethod
    def _parse_price_from_product_page(self):
        '''Parse the Product's Price from the Product Page HTM

        :returns: The Product's Price
        :rtype: :obj:`str`
        '''

    @abstractmethod
    def _parse_weight_from_product_page(self):
        '''Parse the Product's Weight from the Product Page HTM

        :returns: The Product's Weight
        :rtype: :obj:`str`
        '''

    def _get_match_from_product_page(self, regex_string):
        '''Return the first group from the regex in the Product Page's HTML.

        :returns: The first match to the Regular Expression or :obj:`None`
        :rtype: :obj:`str`
        '''
        match = re.search(regex_string, self.page_html)
        if match is not None and match.group(0) is not '':
            return match.group(1)
