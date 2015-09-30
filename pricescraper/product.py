#!/usr/bin/env python3
'''
The Product module holds the class that defines each of SESE's Products and the
respective Products at Other Companies websites.
'''
import settings


class Product(object):
    '''The Product class holds all relevant data for each variety of seed.

    A Product object will contain attributes that hold SESE's information on
    the Product and attributes that hold other companies information on similar
    Products.

    Other companies attributes are named according to the company name::

        companyinital_attribute

    For example, ``bi_name`` refers to the name of BotanicalInterests.com's
    most similar variety. The current abbreviations/initials are:

    * ``bi`` - BotanicalInterests


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
    '''

    def __init__(self, number, name, category, organic):
        '''A Product object is initialized by setting the SESE attributes for
        the Product variety.
        '''
        self.sese_number = number
        self.sese_name = name
        self.sese_category = category
        self.sese_organic = organic.lower() == 'true'

    def get_attribute_list(self):
        '''Return a list containing this Product's SESE and Other attributes

        This order of attributes in the list is determined by the
        :data:`~settings.SESE_HEADER_ORDER`,
        :data:`~settings.COMPANY_HEADER_ORDER` and
        :data:`~settings.ATTRIBUTE_HEADER_ORDER` settings.

        :returns: The SESE and Other Companies Attributes
        :rtype: :obj:`list`
        '''
        attribute_list = list()
        for sese_attribute in settings.SESE_HEADER_ORDER:
            attribute_list.append(getattr(self, sese_attribute))
        for company in settings.COMPANY_HEADER_ORDER:
            for attribute in settings.ATTRIBUTE_HEADER_ORDER:
                full_attribute = company + '_' + attribute
                attribute_list.append(getattr(self, full_attribute))
        return attribute_list

    def add_companys_product_attributes(self, company_abbrev, attribute_dict):
        '''The ``add_companys_product_attributes`` method uses an abbreviation
        and dictionary of attributes to dynamically add an Other Company's
        product information to the Product object.

        The added attributes are defined by the
        :data:`~settings.ATTRIBUTE_HEADER_ORDER` setting and the
        ``attribute_dict`` parameter should use all the strings in the
        :data:`~settings.ATTRIBUTE_HEADER_ORDER`.

        :param company_abbrev: The company's abbreviation, this is used as a
                               prefix for each new attribute
        :type company_abbrev: string
        :param attribute_dict: A dictionary using attributes from
                               :data:`~settings.ATTRIBUTE_HEADER_ORDER` as keys
                               and the company's product information as values
        :type attribute_dict: dict
        :returns: :obj:`None`
        '''
        attribute_abbrev = company_abbrev.lower()
        for attribute in settings.ATTRIBUTE_HEADER_ORDER:
            company_attribute = attribute_abbrev + "_" + attribute
            setattr(self, company_attribute, attribute_dict[attribute])
