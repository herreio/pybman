Pybman (*work in progress*)
=============================

Synopsis
--------

This is a python package for interacting with `MPG.PuRe <https://pure.mpg.de>`_ via the `PubMan REST API <https://pure.mpg.de/rest/swagger-ui.html>`_.


Installation
------------

You can simply install this package via `pip <https://pypi.org/project/pybman/>`_:

.. code-block:: shell

    pip install pybman

Usage
-----

.. code-block:: python

    from pybman import Client
    from pybman import extract

    # initialize client
    cl = Client()

    # retrieve data of specific context
    ctx_data = cl.get_data(ctx_id="ctx_924547")

    # show number of records
    len(ctx_data.records)

    # access records via index
    item = ctx_data.records[0]

    # get genre from item
    genre = extract.genre_from_item(item)
    print("GENRE:", genre)

    # get title from item
    title = extract.title_from_item(item)
    print("TITLE:", title)

    # get creators from item
    persons = extract.persons_from_item(item)
    for person in persons:
        role = extract.role_from_creator(person)
        first_name, last_name = extract.persons_name_from_creator(person)
        id_val, id_type = extract.persons_id_from_creator(person)
        print(first_name, last_name, '('+ id_val +')')
