#!/usr/bin/env python3


import unittest

import settings
from pricescraper.product import Product
from pricescraper.util import create_header_list, get_class, remove_punctuation


class TestProductClass(unittest.TestCase):
    def test_instantiation(self):
        '''Instantiating a Product object should set its ``sese`` attributes'''
        product = Product(name='variety name', category='variety category',
                          organic='True', number='12383A')

        self.assertEqual(product.sese_name, 'variety name')
        self.assertEqual(product.sese_category, 'variety category')
        self.assertEqual(product.sese_organic, True)
        self.assertEqual(product.sese_number, '12383A')

    def test_instantiation_organic_false(self):
        '''
        Product class should take strings for the ``organic`` keyword and set
        the attribute as a Boolean.
        '''
        product = Product(name='variety name', category='variety category',
                          organic='False', number='12383A')

        self.assertEqual(product.sese_organic, False)

    def test_add_companys_product_attributes(self):
        '''
        The `add_companys_product_attributes` function should add attributes to
        a Product object in the order of the `_attribute_header_order` class
        attribute.
        '''
        company_abbrev = 'bi'
        company_attribute_dict = {'name': 'companies product',
                                  'number': '12034',
                                  'organic': False,
                                  'weight': '23.12 grams',
                                  'price': '2.45'}
        product = Product(name='variety name', category='variety category',
                          organic='True', number='12383A')

        product.add_companys_product_attributes(company_abbrev,
                                                company_attribute_dict)

        self.assertEqual(product.bi_name, 'companies product')
        self.assertEqual(product.bi_number, '12034')
        self.assertEqual(product.bi_organic, False)
        self.assertEqual(product.bi_weight, '23.12 grams')
        self.assertEqual(product.bi_price, '2.45')

    def test_add_companys_product_attributes_uppercase_abbrev(self):
        '''
        The `add_companys_product_attributes` function should add attributes to
        a Product object in the order of the `_attribute_header_order` class
        attribute.
        The attributes should be lowercase even if the `company_abbrev` is
        uppercase
        '''
        company_abbrev = 'BI'
        company_attribute_dict = {'name': 'companies product',
                                  'number': '12034',
                                  'organic': False,
                                  'weight': '23.12 grams',
                                  'price': '2.45'}
        product = Product(name='variety name', category='variety category',
                          organic='True', number='12383A')

        product.add_companys_product_attributes(company_abbrev,
                                                company_attribute_dict)

        self.assertTrue(hasattr(product, 'bi_name'))
        self.assertTrue(hasattr(product, 'bi_number'))
        self.assertTrue(hasattr(product, 'bi_organic'))
        self.assertTrue(hasattr(product, 'bi_weight'))
        self.assertTrue(hasattr(product, 'bi_price'))

    def test_get_attribute_list_no_sese_or_companies(self):
        '''Will return empty list if told no headers or companies specified'''
        settings.COMPANY_HEADER_ORDER = []
        settings.SESE_HEADER_ORDER = []
        product = Product(name='variety name', category='variety category',
                          organic='True', number='12383A')

        expected = []

        self.assertSequenceEqual(product.get_attribute_list(), expected)

    def test_get_attribute_list_no_companies(self):
        '''Should return just the sese attributes if no companies'''
        settings.COMPANY_HEADER_ORDER = []
        settings.SESE_HEADER_ORDER = ['sese_number', 'sese_organic',
                                      'sese_name', 'sese_category']
        product = Product(name='variety name', category='variety category',
                          organic='True', number='12383A')

        expected = ['12383A', True, 'variety name', 'variety category']

        self.assertSequenceEqual(product.get_attribute_list(), expected)

    def test_get_attribute_list_one_company(self):
        '''Should return the sese then company attributes'''
        settings.COMPANY_HEADER_ORDER = []
        settings.SESE_HEADER_ORDER = ['sese_number', 'sese_organic',
                                      'sese_name', 'sese_category']
        settings.ATTRIBUTE_HEADER_ORDER = ['price', 'weight', 'number', 'name',
                                           'organic']
        settings.COMPANY_HEADER_ORDER = ['bi']

        product = Product(name='variety name', category='variety category',
                          organic='True', number='12383A')
        company_attribute_dict = {'name': 'companies product',
                                  'number': '12034',
                                  'organic': False,
                                  'weight': '23.12 grams',
                                  'price': '2.45'}
        product.add_companys_product_attributes('bi', company_attribute_dict)

        expected = ['12383A', True, 'variety name', 'variety category',
                    '2.45', '23.12 grams', '12034', 'companies product', False]

        self.assertSequenceEqual(product.get_attribute_list(), expected)

    def test_get_attribute_list_multiple_companies(self):
        '''Should return the sese then company attributes, with companies in
        correct order
        '''
        settings.COMPANY_HEADER_ORDER = []
        settings.SESE_HEADER_ORDER = ['sese_number', 'sese_organic',
                                      'sese_name', 'sese_category']
        settings.ATTRIBUTE_HEADER_ORDER = ['price', 'weight', 'number', 'name',
                                           'organic']
        settings.COMPANY_HEADER_ORDER = ['bi', 'ts']

        product = Product(name='variety name', category='variety category',
                          organic='True', number='12383A')
        company_attribute_dict = {'name': 'companies product',
                                  'number': '12034',
                                  'organic': False,
                                  'weight': '23.12 grams',
                                  'price': '2.45'}
        product.add_companys_product_attributes('ts', company_attribute_dict)
        company_attribute_dict = {'name': 'company 1s product',
                                  'number': '28378',
                                  'organic': True,
                                  'weight': '12 seeds',
                                  'price': '189.54'}
        product.add_companys_product_attributes('bi', company_attribute_dict)

        expected = ['12383A', True, 'variety name', 'variety category',
                    '189.54', '12 seeds', '28378', 'company 1s product', True,
                    '2.45', '23.12 grams', '12034', 'companies product', False]

        self.assertSequenceEqual(product.get_attribute_list(), expected)


class TestUtilFunctions(unittest.TestCase):
    '''Tests the ``util`` module'''

    def test_create_header_list_no_company(self):
        '''
        The create_header_list() static method should return a list containing
        the Names of each attribute in the correct order if no Other Companies
        are specified
        '''
        settings.SESE_HEADER_ORDER = ['sese_number', 'sese_organic',
                                      'sese_name', 'sese_category']
        settings.ATTRIBUTE_HEADER_ORDER = ['price', 'weight', 'number', 'name',
                                           'organic']
        settings.COMPANY_HEADER_ORDER = []

        result = create_header_list()
        expected = ['SESE SKU', 'SESE Organic', 'SESE Name', 'SESE Category']

        self.assertSequenceEqual(expected, result)

    def test_create_header_list_one_company(self):
        '''
        The create_header_list() static method should return a list containing
        the Names of each attribute in the correct order if only one Other
        Company is specified
        '''
        settings.SESE_HEADER_ORDER = ['sese_number', 'sese_organic',
                                      'sese_name', 'sese_category']
        settings.ATTRIBUTE_HEADER_ORDER = ['price', 'weight', 'number', 'name',
                                           'organic']
        settings.COMPANY_HEADER_ORDER = ['bi']

        result = create_header_list()
        expected = ['SESE SKU', 'SESE Organic', 'SESE Name', 'SESE Category',
                    'BI Price', 'BI Weight', 'BI ID#', 'BI Name', 'BI Organic']

        self.assertSequenceEqual(expected, result)

    def test_create_header_list_multiple_companies(self):
        '''
        The create_header_list() static method should return a list containing
        the Names of each attribute in the correct order if multiple Other
        Companies are specified
        '''
        settings.SESE_HEADER_ORDER = ['sese_number', 'sese_organic',
                                      'sese_name', 'sese_category']
        settings.ATTRIBUTE_HEADER_ORDER = ['price', 'weight', 'number', 'name',
                                           'organic']
        settings.COMPANY_HEADER_ORDER = ['bi', 'ts']

        result = create_header_list()
        expected = ['SESE SKU', 'SESE Organic', 'SESE Name', 'SESE Category',
                    'BI Price', 'BI Weight', 'BI ID#', 'BI Name', 'BI Organic',
                    'TS Price', 'TS Weight', 'TS ID#', 'TS Name', 'TS Organic']

        self.assertSequenceEqual(expected, result)

    def test_get_class(self):
        '''Should return the correct Class'''
        self.assertEqual(get_class('pricescraper.product.Product'), Product)

    def test_remove_punctuation(self):
        '''Should remove all punctuation from the string'''
        result = remove_punctuation('!d$k>&<l,;.')
        self.assertEqual(result, 'dkl')
