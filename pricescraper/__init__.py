'''
The PriceScraper Module is designed to scrape prices from competitors websites.

It is used to aid us in comparing our seed prices with competitors.

Websites to scrape are defined in the :mod:`sites` module. Each website is
represented by a class that inherits from the :class:`sites.base.BaseSite`
class. Each object in this class represents a specific Product on the
competitors website, storing details such as it's name, model number, price and
weight.

Our(SESE's) attributes are defined by the :class:`Product` class. Each object
of this class represents a distinct Seed Variety at SESE. Each Product object
will create one object for every class that inherits from
:class:`sites.base.BaseSite`. The Product object will absorb the detail
extracted by the Site objects and prepare it for output.

The overarching input, object creation and output are controlled by the
:mod:`price_scraper` module which reads SESE's products and outputs the scraped
data from/to CSV files.
'''
