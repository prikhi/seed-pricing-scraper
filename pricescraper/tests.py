#!/usr/bin/env python3


import unittest

from pricescraper.product import Product


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

    def test_create_header_list_no_company(self):
        '''
        The create_header_list() static method should return a list containing
        the Names of each attribute in the correct order if no Other Companies
        are specified
        '''
        Product._sese_header_order = ['sese_number', 'sese_organic',
                                      'sese_name', 'sese_category']
        Product._attribute_header_order = ['price', 'weight', 'number', 'name',
                                           'organic']
        Product._company_header_order = []

        result = Product.create_header_list()
        expected = ['SESE SKU', 'SESE Organic', 'SESE Name', 'SESE Category']

        self.assertSequenceEqual(expected, result)

    def test_create_header_list_one_company(self):
        '''
        The create_header_list() static method should return a list containing
        the Names of each attribute in the correct order if only one Other
        Company is specified
        '''
        Product._sese_header_order = ['sese_number', 'sese_organic',
                                      'sese_name', 'sese_category']
        Product._attribute_header_order = ['price', 'weight', 'number', 'name',
                                           'organic']
        Product._company_header_order = ['bi']

        result = Product.create_header_list()
        expected = ['SESE SKU', 'SESE Organic', 'SESE Name', 'SESE Category',
                    'BI Price', 'BI Weight', 'BI ID#', 'BI Name', 'BI Organic']

        self.assertSequenceEqual(expected, result)

    def test_create_header_list_multiple_companies(self):
        '''
        The create_header_list() static method should return a list containing
        the Names of each attribute in the correct order if multiple Other
        Companies are specified
        '''
        Product._sese_header_order = ['sese_number', 'sese_organic',
                                      'sese_name', 'sese_category']
        Product._attribute_header_order = ['price', 'weight', 'number', 'name',
                                           'organic']
        Product._company_header_order = ['bi', 'ts']

        result = Product.create_header_list()
        expected = ['SESE SKU', 'SESE Organic', 'SESE Name', 'SESE Category',
                    'BI Price', 'BI Weight', 'BI ID#', 'BI Name', 'BI Organic',
                    'TS Price', 'TS Weight', 'TS ID#', 'TS Name', 'TS Organic']

        self.assertSequenceEqual(expected, result)

    def test_add_companys_product_attributes(self):
        '''
        The `add_companys_product_attributes` function should add attributes to
        a Product object in the order of the `_attribute_header_order` class
        attribute.
        '''
        Product._sese_header_order = ['sese_number', 'sese_organic',
                                      'sese_name', 'sese_category']
        Product._attribute_header_order = ['price', 'weight', 'number', 'name',
                                           'organic']
        Product._company_header_order = ['bi']
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
        Product._sese_header_order = ['sese_number', 'sese_organic',
                                      'sese_name', 'sese_category']
        Product._attribute_header_order = ['price', 'weight', 'number', 'name',
                                           'organic']
        Product._company_header_order = ['bi']
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
