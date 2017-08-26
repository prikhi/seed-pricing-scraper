====================
Seed Pricing Scraper
====================


.. image:: https://readthedocs.org/projects/seed-pricing-scraper/badge/?version=latest
    :target: http://seed-pricing-scraper.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
                

This scrapes various seed company websites for product information & prices.

It uses Python 3, along with Sphinx for documentation & Nose for testing.


Quickstart
==========

Change into the ``pricescraper`` directory::

    cd pricescraper

Stick a CSV named ``input.csv`` containing your Product's SKU, Name, Category,
& Organic Status into the directory::

    mv ~/input.csv .

Run the scraper::

    python price_scraper.py


Building the Docs
=================

You can install the required dependencies using ``pip``, it's recommended to do
this in a virtual environment::

    python -m venv Env
    source Env/bin/activate
    pip install -r requirements/develop.txt

Then build the docs::

    cd docs/
    make html
    firefox _build/html/index.html

You can also build a PDF of the documentation by running ``make latexpdf``
instead.
