Installation
-------------

These instructions are for \*nix systems, Windows has not been tested but may
be supported.


Installing the Price Scraper requires that you have the following software
on your system:

* git
* python3
* pip or setuptools

Optionally, virtualenv and virtualenvwrapper will make dependency management
and isolation much easier.

These can be installed using your systems package manager. Virtualenv and
Virtualenvwrapper can be installed using pip. For example, Arch Linux users can
simply run the following:

.. code-block:: sh

    $ sudo pacman -S python pip3 git
    $ sudo pip install virtualenv virtualenvwrapper

Once you have these dependencies, you should clone the source code repository:

.. code-block:: sh

    $ git clone git@aphrodite.acorn:/srv/git/pricescraper.git pricescraper
    $ cd pricescraper


This will create a local copy of all the source files. If you have virtualenv
installed you should now make a new virtual environment, using your python3
binary:

.. code-block:: sh

    $ mkvirtualenv PriceScraper -p python3

You can then install the python dependencies into your system or the new
virtual environment using pip and our requirements files:

.. code-block:: sh

    $ pip install -r requirements/develop.txt

Use ``develop.txt`` to include development dependencies, such as the test
runner and documentation builder. If you just want to run the application,
you may use ``requirements/base.txt`` instead.

After all dependencies are installed by pip, you should be able to run the
application using a valid input file(tab-delimited, containing a header row
and columns for SESE SKU, Organic Status, Name and Category):

.. code-block:: sh

    $ python3 pricescraper/price_scraper.py
