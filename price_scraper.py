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
import urllib.parse
import urllib.request


BOTANICAL_ROOT = 'http://www.botanicalinterests.com'
BOTANICAL_SEARCH = 'http://www.botanicalinterests.com/products/index/srch:'
BOTANICAL_NO_RESULT_TEXT = ("Sorry, we couldn&rsquo;t find any pages that "
                            "matched your criteria.")


class Product(object):
    def __init__(self, sku, name, category, organic):
        '''Initialize the Products data and retrieve information from sites.'''
        self.sku = sku
        self.name = name
        self.category = category
        if organic.lower() == 'true':
            self.organic = True
        else:
            self.organic = False

        self.botanical_name = self.botanical_number = ""
        self.botanical_price = self.botanical_weight = ""
        self.botanical_organic = False

        self.fetch_botanical_information()

    def fetch_botanical_information(self):
        '''
        Fetches the Product's Page on the Botanical Interests website, setting
        Product attributes, depending on whether or not a product was found.
        '''
        search_term = "{} {}".format(self.name, self.category)
        if self.organic:
            search_term += " Organic"
        product_page = search_botanical_site(search_term)
        if product_page is None:
            self.botanical_number = "Not Found"
            return
        self.botanical_name = product_page.split("<title>")[1].split(
            "</title>")[0].split("|")[0]
        self.botanical_number = product_page.split(
            'class="item_num">Item #')[1].split("</p>")[0]
        self.botanical_price = product_page.split("$")[1].split(
            "</h2>")[0].split()[0]
        self.botanical_weight = product_page.split('Item #')[2].split(
            "</p>")[1].split("<p>")[1]
        if "organic" in self.botanical_name.lower():
            self.botanical_organic = True

    def create_csv_line(self, csvwriter):
        '''
        Adds the Product's attributes as a line in the specified csv_file

        The following order will be used:
            1. Our ID
            2. Our Organic Status
            3. Our Variety Name
            4. Our Category Name
            5. Botanical Price/Packet
            6. Botanical Grams/Packet
            7. Botanical ID Number
            8. Botanical Name
            9. Botanical Organic Status
        '''
        csv_row = [self.sku, self.organic, self.name, self.category,
                   self.botanical_price, self.botanical_weight,
                   self.botanical_number, self.botanical_name,
                   self.botanical_organic]
        csvwriter.writerow(csv_row)


def search_botanical_site(search_keywords):
    '''
    Searches the Botanical Interests site for the keyword

    Returns the HTML of the first result, or None if no result was found.
    '''
    encoded_keywords = urllib.parse.quote(search_keywords)
    search_url = BOTANICAL_SEARCH + encoded_keywords
    request = urllib.request.Request(search_url, headers={'User-Agent':
                                                          'Mozilla/5.0'})
    result_page = str(urllib.request.urlopen(request).read())
    if BOTANICAL_NO_RESULT_TEXT in result_page:
        return None
    # Split HTML to get link to first result
    product_link = result_page.split('<div class="list-thumb">')[1].split(
        'href="')[1].split('"')[0]
    full_link = BOTANICAL_ROOT + product_link

    request = urllib.request.Request(full_link, headers={'User-Agent':
                                                         'Mozilla/5.0'})
    product_page = str(urllib.request.urlopen(request).read())
    return product_page


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
            product = Product(sku=row[0], organic=row[1],
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
        header_row = ["SESE SKU", "SESE Organic", "SESE Name", "SESE Category",
                      "BI Price", "BI Weight", "BI ID#", "BI Name",
                      "BI Organic"]
        outputwriter.writerow(header_row)
        for product in product_objects:
            product.create_csv_line(outputwriter)


def main():
    '''
    Loads the input file and exports the Product object details
    '''
    product_objects = load_input_file('./input.csv')
    create_output_file('./output.csv', product_objects)

if __name__ == '__main__':
    main()
