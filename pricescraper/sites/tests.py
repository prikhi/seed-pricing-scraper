'''This module contains unit tests for the Sites Package'''

import unittest

from .base import BaseSite
from .botanical_interests import (BotanicalInterests,
                                  get_results_from_search_page)
from .testfixtures import botanical_fixtures


class BaseSiteTests(unittest.TestCase):
    '''Test the abstract BaseSite class'''
    class MockSite(BaseSite):
        '''Create a mock class to test the BaseSite class'''
        def __init__(self, *args, **kwargs):
            super(BaseSiteTests.MockSite, self).__init__(*args, **kwargs)
            self.page_html = ''
        def _find_product_page(self):
            pass

        def _get_best_match_or_none(self, search_page_html):
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
        mock_object._parse_and_set_attributes()

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
        mock_object._parse_and_set_attributes()

        self.assertEqual(mock_object.name, 'Not Found')
        self.assertEqual(mock_object.number, None)
        self.assertEqual(mock_object.organic, None)
        self.assertEqual(mock_object.price, None)
        self.assertEqual(mock_object.weight, None)

    def test_get_company_attributes_unset(self):
        '''The attributes should default to None if not set'''
        mock_object = self.MockSite('sese name', 'sese category',
                                    'sese organic')
        expected = {'name': None,
                    'number': None,
                    'organic': None,
                    'price': None,
                    'weight': None}
        self.assertEqual(expected, mock_object.get_company_attributes())

    def test_get_company_attributes_set(self):
        '''The attributes should be returned if set'''
        mock_object = self.MockSite('sese name', 'sese category',
                                    'sese organic')
        mock_object._parse_and_set_attributes()
        expected = {'name': 'name',
                    'number': 'number',
                    'organic': 'organic',
                    'price': 'price',
                    'weight': 'weight'}
        self.assertEqual(expected, mock_object.get_company_attributes())


class BotanicalInterestsTests(unittest.TestCase):
    '''Test the BotanicalInterests Class'''
    def setUp(self):
        '''Load the HTML files'''
        self.NO_RESULT_HTML = botanical_fixtures.NO_RESULT_HTML
        self.RESULTS_HTML = botanical_fixtures.RESULTS_HTML
        self.SEEDS_HTML = botanical_fixtures.SEEDS_HTML
        self.GRAMS_HTML = botanical_fixtures.GRAMS_HTML
        self.ORGANIC_HTML = botanical_fixtures.ORGANIC_HTML

    def test_get_results_from_search_page(self):
        expected = [
                ('/products/view/3130/Tomato-Pole-Brandywine-Red-Yellow-Organic-HEIRLOOM-Seeds/srch:brandywine organic',
                 'Tomato Pole Brandywine Red &amp; Yellow Organic HEIRLOOM Seeds'),
                ('/products/view/0051/Tomato-Pole-Brandywine-HEIRLOOM-Seeds/srch:brandywine organic',
                 'Tomato Pole Brandywine HEIRLOOM Seeds'),
                ('/products/view/4560/Heirloom-Organic-Seed-Bank-Collection/srch:brandywine organic',
                 'Heirloom Organic Seed Bank Collection'),
                ('/products/view/3044/Edamame-Butterbean-Organic-Seeds/srch:brandywine organic',
                 'Edamame Butterbean Organic Seeds'),
                ('/products/view/3113/Pumpkin-Howden-Organic-Seeds/srch:brandywine organic',
                 'Pumpkin Howden Organic Seeds'),
                ('/products/view/2014/Sunflower-Sunspot-Organic-Seeds/srch:brandywine organic',
                 'Sunflower Sunspot Organic Seeds'),
                ('/products/view/3071/Pumpkin-Big-Max-Organic-HEIRLOOM-Seeds/srch:brandywine organic',
                 'Pumpkin Big Max Organic HEIRLOOM Seeds'),
                ('/products/view/2021/Butterfly-Flower-Organic-Seeds/srch:brandywine organic',
                 'Butterfly Flower Organic Seeds'),
                ('/products/view/3123/Cucumber-Marketmore-Organic-Seeds/srch:brandywine organic',
                 'Cucumber Marketmore Organic Seeds'),
                ('/products/view/6098/Lovage-Organic-HEIRLOOM-Seeds/srch:brandywine organic',
                 'Lovage Organic HEIRLOOM Seeds'),
                ('/products/view/6064/Catnip-Organic-HEIRLOOM-Seeds/srch:brandywine organic',
                 'Catnip Organic HEIRLOOM Seeds'),
                ('/products/view/2005/Feverfew-Organic-HEIRLOOM-Seeds/srch:brandywine organic',
                 'Feverfew Organic HEIRLOOM Seeds'),
                ('/products/view/6127/Borage-Organic-HEIRLOOM-Seeds/srch:brandywine organic',
                 'Borage Organic HEIRLOOM Seeds'),
                ('/products/view/6080/Marjoram-Organic-HEIRLOOM-Seeds/srch:brandywine organic',
                 'Marjoram Organic HEIRLOOM Seeds'),
                ('/products/view/3052/Lettuce-Butterhead-Buttercrunch-Organic-Seeds/srch:brandywine organic',
                 'Lettuce Butterhead Buttercrunch Organic Seeds'),
                ('/products/view/6078/Lemon-Balm-Organic-HEIRLOOM-Seeds/srch:brandywine organic',
                 'Lemon Balm Organic HEIRLOOM Seeds'),
                ('/products/view/6062/Chives-Common-Organic-HEIRLOOM-Seeds/srch:brandywine organic',
                 'Chives Common Organic HEIRLOOM Seeds'),
                ('/products/view/3014/Beet-Early-Wonder-Organic-HEIRLOOM-Seeds/srch:brandywine organic',
                 'Beet Early Wonder Organic HEIRLOOM Seeds'),
                ('/products/view/2020/Pepper-on-a-Stick-Ornamental-Organic-Seeds/srch:brandywine organic',
                 'Pepper on a Stick Ornamental Organic Seeds'),
                ('/products/view/3035/Cucumber-Straight-Eight-Organic-HEIRLOOM-Seeds/srch:brandywine organic',
                 'Cucumber Straight Eight Organic HEIRLOOM Seeds')]

        self.assertEqual(expected,
                         get_results_from_search_page(self.RESULTS_HTML))

    def test_parse_name_from_product_page(self):
        '''Tests that the Name REGEX works correctly'''
        product = BotanicalInterests('sese name', 'sese cat', True)
        product.page_html = self.SEEDS_HTML

        name = product._parse_name_from_product_page()

        self.assertEqual("Tomato Pole Brandywine HEIRLOOM Seeds", name)

    def test_parse_number_from_product_page(self):
        '''Tests that the Number REGEX works correctly'''
        product = BotanicalInterests('sese number', 'sese cat', True)
        product.page_html = self.SEEDS_HTML

        number = product._parse_number_from_product_page()

        self.assertEqual("0051", number)

    def test_parse_organic_from_product_page_true(self):
        '''Tests that the Products Organic attribute is set to True if Organic
        is in the Name'''
        product = BotanicalInterests('sese name', 'sese cat', True)
        product.page_html = self.ORGANIC_HTML
        product.name = product._parse_name_from_product_page()

        organic = product._parse_organic_status_from_product_page()

        self.assertIn('organic', product.name.lower())
        self.assertTrue(organic)

    def test_parse_organic_from_product_page_false(self):
        '''Tests that the Products Organic attribute is set to False if Organic
        is not in the Name'''
        product = BotanicalInterests('sese name', 'sese cat', True)
        product.page_html = self.SEEDS_HTML
        product.name = product._parse_name_from_product_page()

        organic = product._parse_organic_status_from_product_page()

        self.assertNotIn('organic', product.name.lower())
        self.assertFalse(organic)

    def test_parse_price_from_product_page(self):
        '''Tests that the Price REGEX works correctly'''
        product = BotanicalInterests('sese name', 'sese cat', True)
        product.page_html = self.SEEDS_HTML

        price = product._parse_price_from_product_page()

        self.assertEqual("1.89", price)

    def test_parse_weight_from_product_page_grams(self):
        '''Tests that the Weight REGEX works for weights in grams'''
        product = BotanicalInterests('sese name', 'sese cat', True)
        product.page_html = self.GRAMS_HTML

        grams = product._parse_weight_from_product_page()

        self.assertEqual("251.72 grams", grams)

    def test_parse_weight_from_product_page_seeds(self):
        '''Tests that the Weight REGEX works for weights in seeds'''
        product = BotanicalInterests('sese name', 'sese cat', True)
        product.page_html = self.SEEDS_HTML

        seeds = product._parse_weight_from_product_page()

        self.assertEqual("30 seeds", seeds)

    def test_get_match_from_product_pages_no_match(self):
        '''Return None if no match in page'''
        product = BotanicalInterests('sese name', 'sese cat', True)
        product.page_html = ''

        matches = product._get_match_from_product_page(r'.*')

        self.assertIsNone(matches)
