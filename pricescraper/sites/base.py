#!/usr/bin/env python
from abc import abstractmethod, ABCMeta


class BaseSite(object):
    '''The BaseSite class is an Abstract class for creating new Site classes.

    For each website that needs to be scraped, a Class should be created,
    inheriting and implementing this Abstract Base class.

    The following class attributes are recommended:
        * _COMPANY_ABBREVIATION
        * _ROOT_URL
        * _SEARCH_URL
        * _NO_RESULT_TEXT

    The product page searching and parsing methods must be implemented by any
    of this Classes children.
    '''
    __metaclass__ = ABCMeta
    _COMPANY_ABBREVIATION = str()

    _ROOT_URL = str()
    _SEARCH_URL = str()
    _NO_RESULT_TEXT = str()

    def __init__(self, name, category, organic):
        '''The Constructor finds the Product's Page and sets its attributes

        :param name: SESE's name for this Product
        :type name: string
        :param category: SESE's category for this Product
        :type category: string
        :param organic: SESE's organic status for this Product
        :returns: :obj:`None`
        '''
        self._set_sese_attributes(name, category, organic)
        self.page_html = self._find_product_page()
        self._parse_and_set_company_attributes()

    def _set_sese_attributes(self, name, category, organic):
        '''Sets the supplied variables as SESE's attributes

        :param name: SESE's name for this Product
        :type name: string
        :param category: SESE's category for this Product
        :type category: string
        :param organic: SESE's organic status for this Product
        :returns: :obj:`None`
        '''
        self.sese_name = name
        self.sese_category = category
        self.sese_organic = organic

    def _parse_and_set_company_attributes(self):
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

    def get_company_attributes(self):
        '''Return a dictionary containing this Company's Product attributes

        :raises: AttributeError if the name, number, organic status, price or
                 weight have not been set.
        '''
        return {'name': self.name,
                'number': self.number,
                'organic': self.organic,
                'price': self.price,
                'weight': self.weight}

    @abstractmethod
    def _find_product_page(self):
        '''Find the Product Page from the Company's website.

        :returns: The Product Page's HTML
        :rtype: string
        '''

    @abstractmethod
    def _search_site(self, search_terms):
        '''Search the Company's website using the provided ``search_terms``

        :param search_terms: The keywords to search for
        :type search_terms: string
        :returns: The Search Result Page's HTML
        :rtype: string
        '''

    @abstractmethod
    def _get_best_match_or_none(self, search_page_html):
        '''Attempt to find the best match on the Search Page

        :param search_page_html: The Search Results Page's HTML
        :type search_page_html: string
        :returns: URL of the best match or None if no good match
        :rtype: string or :obj:`None`
        '''

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
