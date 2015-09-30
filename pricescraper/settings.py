'''This module defines the basic settings used throughout the application.'''


#: The minimum percentage of words in common between SESE's and Other Company's
#: Product names for them to be considered a match.
MINIMUM_NAME_MATCHING_PERCENTAGE = 36

#: The Other Company's to process (by path to Class)
COMPANIES_TO_PROCESS = [
    'sites.botanical_interests.BotanicalInterests',
]

#: The output order of the Other Companies (by abbrieviation)
COMPANY_HEADER_ORDER = (
    'bi',
)

#: The output order of each Other Company's attributes
ATTRIBUTE_HEADER_ORDER = (
    'price', 'weight', 'number', 'name', 'organic'
)

#: The output order of SESE attributes
SESE_HEADER_ORDER = (
    'sese_number', 'sese_organic', 'sese_name', 'sese_category'
)

#: A dictionary mapping attributes to display names
ATTRIBUTES_TO_NAMES = {
    'sese_number': "SESE SKU",
    'sese_organic': "SESE Organic",
    'sese_name':   "SESE Name",
    'sese_category': "SESE Category",
    'name': "Name",
    'number': "ID#",
    'weight': "Weight",
    'price': "Price",
    'organic': "Organic"
}
