#!/usr/bin/env python3
'''
This Script pulls data about the Price and Weight of Seed Packets from
BotanicalInterests.com

It requires a file named `input.csv` to be in the same directory.
This `input.csv` file should be a Tab-delimited CSV, with fields for each
Product's SKU, Organic Status(True or False), Variety Name and Category.

The Script will take these Products, search BotanicalInterests.com using the
Variety Name and Category, and create a Tab-delimited CSV containing BI.com's
Packet Price, Packet Weight, Item Number, Item Name and Organic Status.

The Script uses best matches, not exact matches, so the data should be reviewed
afterwards.


Written by Pavan Rikhi<pavan.rikhi@gmail.com> on 10/10/2013 for Acorn Community
'''
import csv

from product import Product
import settings
from util import create_header_list, get_class


def load_input_file(filename):
    '''
    Reads the input CSV, creating Product objects from each line.

    Assumes the input file is seperated by commas and contains the product's
    SKU, Name, Variety Category and Organic Status(True or False)

    Returns a list of the Product objects that were created.
    '''
    product_objects = list()

    with open(filename, 'r', encoding="utf8") as csvfile:
        input_reader = csv.reader(csvfile, delimiter='\t')
        input_reader.__next__()   # Skip the header line
        for row in input_reader:
            product = Product(number=row[0], organic=row[1],
                              name=row[2], category=row[3])
            product_objects.append(product)

    return product_objects


def create_output_file(filename, product_objects):
    '''
    Iterates through a products list, creating a CSV file where each line
    contains a Product's SKU, Name, Category, Organic Status and the Name,
    Number, Price and Weight of the related Product from each competitor's
    site.
    '''
    with open(filename, 'w', encoding="utf8") as csvfile:
        outputwriter = csv.writer(csvfile, delimiter='\t')
        header_row = create_header_list()
        outputwriter.writerow(header_row)
        for product in product_objects:
            products_attributes = product.get_attribute_list()
            outputwriter.writerow(products_attributes)


def main():
    '''
    Loads the input file and exports the Product object details
    '''
    product_objects = load_input_file('./input.csv')

    for product in product_objects:
        for website in settings.COMPANIES_TO_PROCESS:
            website = get_class(website)
            website_product = website(product.sese_name,
                                      product.sese_category,
                                      product.sese_organic)
            website_product.get_and_set_product_information()
            attributes = website_product.get_company_attributes()
            product.add_companys_product_attributes(website.ABBREVIATION,
                                                    attributes)

    create_output_file('./output.csv', product_objects)

if __name__ == '__main__':
    main()
