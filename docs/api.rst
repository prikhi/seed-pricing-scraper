==================
API Documentation
==================


The following page describes the Classes and Functions used by the Price
Scraper program.


.. _product_module:

:mod:`product` Module
----------------------

.. automodule:: product
    :members:

.. _settings_module:

:mod:`settings` Module
-----------------------

.. automodule:: settings
    :members:


.. _util_module:

:mod:`util` Module
-------------------

.. automodule:: util
    :members:


.. _sites_module:

:mod:`sites` Module
--------------------


The :ref:`sites<sites_module>` module contains Classes that describe the website the program
will scrape. Searching and Parsing for each website is defined by a class that
inherits from the :class:`~sites.base.BaseSite` Class. One object will
represent a single Product from the Other Company/Website.

Upon initialization, each Object will visit the Other Company's website, find
the Product that best matches the provided Name, Category and Organic Status
and scrape the Product's details, such as its name, organic status, model
number, weight and price.

The :meth:`~sites.base.BaseSite.get_company_attributes` method from each child
Class can be used to retrieve the information about the Other Company's
Product.

:mod:`~sites.base` Module
++++++++++++++++++++++++++

.. automodule:: sites.base
    :members:
    :private-members:

:mod:`~sites.botanical_interests` Module
+++++++++++++++++++++++++++++++++++++++++

.. automodule:: sites.botanical_interests
    :members:
    :private-members:
