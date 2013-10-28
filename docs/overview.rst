Overview
=========

SESE's Price Scraper is a Python application that was built to scrape
competitor's website for price information. SESE uses this information to
determine the degree of our yearly price increases for each variety of seed we
have.

When run, the application reads a tab-delimited file containing the SKU#, name,
category and organic status of each of our products. It uses this information
to create a :class:`~product.Product` object for each SESE product.

Each :class:`~product.Product` object creates a new object for each website to
scrape. These objects are from classes that sub-class the
:class:`~sites.base.BaseSite` abstract class, such as the
:class:`~sites.botanical_interests.BotanicalInterests` class. The website
classes implement the specific functionality for scraping a single website for
a single product.

After every :class:`~product.Product` object has created all it's website
objects, the application runs through each :class:`~product.Product` object,
creating a tab-delimited file as the output.

In order to add additional websites for the application to scrape, a new
website class should be created, sub-classing :class:`~sites.base.BaseSite`.
Next, the :mod:`settings` module should be edited so that the
:data:`~settings.COMPANY_HEADER_ORDER` setting contains the abbreviation of the
new website, and the :data:`~settings.COMPANIES_TO_PROCESS` setting contains the
path to the website's implementation class, for example
``sites.botanical_interests.BotanicalInterests``.

