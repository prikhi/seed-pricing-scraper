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
