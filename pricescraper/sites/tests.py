'''This module contains unit tests for the Sites Package'''

import unittest

from pricescraper.sites.base import BaseSite


class BaseSiteTests(unittest.TestCase):
    '''Test the abstract BaseSite class'''
    class MockSite(BaseSite):
        '''Create a mock class to test the BaseSite class'''
        def __init__(self, name, category, organic):
            self._set_sese_attributes(name, category, organic)

        def _find_product_page(self):
            pass

        def _search_site(self):
            pass

        def _get_best_match_or_none(self):
            pass

        def _parse_name_from_product_page(self):
            return 'name'

        def _parse_number_from_product_page(self):
            return 'number'

        def _parse_organic_status_from_product_page(self):
            return 'organic'

        def _parse_price_from_product_page(self):
            return 'price'

        def _parse_weight_from_product_page(self):
            return 'weight'

    def test_class_is_abstract(self):
        '''The BaseSite class should not be able to be instantiated.'''
        self.assertRaises(TypeError, BaseSite, kwargs={'name': 'test name',
                                                       'category': 'stuff',
                                                       'organic': True})

    def test_parse_and_set_company_attributes(self):
        '''This function should set the name, number, organic status, price and
        weight attributes using the _parse methods if a Product Page is found,
        which is denoted by `self.page_html` not being `None`.
        '''
        mock_object = self.MockSite('sese name', 'sese category',
                                    'sese organic')
        mock_object.page_html = "required to set attributes correctly"
        mock_object._parse_and_set_company_attributes()

        self.assertEqual(mock_object.name, 'name')
        self.assertEqual(mock_object.number, 'number')
        self.assertEqual(mock_object.organic, 'organic')
        self.assertEqual(mock_object.price, 'price')
        self.assertEqual(mock_object.weight, 'weight')

    def test_parse_and_set_company_attributes_no_product_page_html(self):
        '''If no Product Page is found, set the attributes accordingly'''
        mock_object = self.MockSite('sese name', 'sese category',
                                    'sese organic')
        mock_object.page_html = None
        mock_object._parse_and_set_company_attributes()

        self.assertEqual(mock_object.name, 'Not Found')
        self.assertEqual(mock_object.number, None)
        self.assertEqual(mock_object.organic, None)
        self.assertEqual(mock_object.price, None)
        self.assertEqual(mock_object.weight, None)

    def test_get_company_attributes_attribute_error(self):
        '''If the attributes are not set raise an AttributeError.'''
        mock_object = self.MockSite('sese name', 'sese category',
                                    'sese organic')
        self.assertRaises(AttributeError, mock_object.get_company_attributes)
