#!/usr/bin/env python3
'''
This module describes the :class:`Product` class.
'''


attribute_to_name = {'sese_number': "SESE SKU",
                     'sese_organic': "SESE Organic",
                     'sese_name':   "SESE Name",
                     'sese_category': "SESE Category",
                     'name': "Name",
                     'number': "ID#",
                     'weight': "Weight",
                     'price': "Price",
                     'organic': "Organic"
                     }


class Product(object):
    '''
    Product hold all relevant data for each variety of seed.

    A Product object will contain attributes that hold SESE's information on
    the Product and attributes that hold other companies information on similar
    Products.

    Other companies attributes are named according to the company name::

        companyinital_attribute

    For example, ``bi_name`` refers to the name of BotanicalInterests.com's
    most similar variety. The abbreviations/initials are::

        * ``bi`` - BotanicalInterests
        * ``rg`` - Renee's Garden
        * ``js`` - Johnny's Seeds
        * ``ts`` - Territorial Seeds

    .. attribute:: sese_name

        Our variety name for the product

    .. attribute:: sese_number

        Our SKU/Model Number for the product

    .. attribute:: sese_category

        Our category for the product

    .. attribute:: sese_organic

        Our organic status for the product

    .. attribute:: company_name

        A company's variety name for the product

    .. attribute:: company_number

        A company's model number for the product

    .. attribute:: company_price

        A company's price per packet for the product

    .. attribute:: company_weight

        A company's grams per packet or seeds per packet for the product

    .. attribute:: company_organic

        A company's organic status for their product

    .. attribute:: _sese_header_order

        A list of strings which defines the order that SESE attributes are
        exported

    .. attribute:: _company_header_order

        A list of strings which defines the order that Other Companies are
        exported

    .. attribute:: _attribute_header_order

        A list of strings which defines the order that Other Company attributes
        are exported

    '''
    _sese_header_order = ['sese_number', 'sese_organic', 'sese_name',
                          'sese_category']
    _company_header_order = ['bi']
    _attribute_header_order = ['price', 'weight', 'number', 'name', 'organic']

    def __init__(self, number, name, category, organic):
        self.sese_number = number
        self.sese_name = name
        self.sese_category = category
        self.sese_organic = organic.lower() == 'true'

    @staticmethod
    def create_header_list():
        header_list = []
        for sese_header in Product._sese_header_order:
            header_list.append(attribute_to_name[sese_header])
        for company in Product._company_header_order:
            company_abbrev = company.upper()
            for attribute in Product._attribute_header_order:
                attribute_name = attribute_to_name[attribute]
                header_name = " ".join([company_abbrev, attribute_name])
                header_list.append(header_name)
        return header_list
