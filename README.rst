.. role:: shell(code)
   :language: shell

Pybman
=============================

Synopsis
--------

This is a Python package for interacting with `MPG.PuRe <https://pure.mpg.de>`_ via the `PubMan REST API <https://pure.mpg.de/rest/swagger-ui.html>`_.

Installation
------------

You can simply install this package via `PyPI <https://pypi.org/project/pybman/>`_:

.. code-block:: shell

    pip install pybman

... or by cloning the repository:

.. code-block:: shell

    git clone https://github.com/herreio/pybman.git
    cd pybman

Documentation
-------------

A minimal documentation can be found on `Read the Docs <https://pybman.readthedocs.io/>`_.

Usage
-----

Launch the Python interpreter and start by importing the necessary modules:

.. code-block:: python

    from pybman import Client
    from pybman import extract

    # initialize client
    cl = Client()

    # retrieve data of specific context
    ctx = cl.get_data(ctx_id="ctx_924547")
    
    # number of records in this context
    num_records = ctx.num

    # access records via index
    item = ctx.records[0]

    # get genre from item ...
    genre = extract.genre_from_item(item)
    print("GENRE:", genre)

    # ... or get genres and associated items from context
    genres = ctx.get_genres()
    
    # list all genres used in this context
    list(genres.keys())

    # get all articles (list of item IDs) from context
    articles = genres['ARTICLE']

    # get data of item (article) by id
    item = ctx.get_item(articles[0])

    # get title from item
    title = extract.title_from_item(item)
    print("TITLE:", title)

    # get publication date from item
    date = extract.date_from_item(item)
    print("PUBLISHED:", date)

    # get creators (persons) from item
    persons = extract.persons_from_item(item)
    for person in persons:
        role = extract.role_from_creator(person)
        first_name, last_name = extract.persons_name_from_creator(person)
        id_val, id_type = extract.persons_id_from_creator(person)
        print(role+':', first_name, last_name, '('+ id_val +')')


Beside data retrieval and browsing Pybman also allows to update items! Because this process requires certain rights, you have to provide credentials. The easiest way is to create a `secret.json <./conf/secret.json>`_ file with your PuRe login (:code:`userName:userPassword`) and hand in the path pointing to it when creating the client instance. (Please use a different location for storing the :code:`secret.json`-file than the one in this repo as it will be tracked by git or alternatively tell git before editing the file to not take care of your changes by running the command :shell:`git update-index --assume-unchanged conf/secret.json`.)


.. code-block:: python

    # intialize client instance (login)
    cl_auth = Client(secret="./conf/secret.json")

    # retrieve context you are allowed to modify
    ctx = cl_auth.get_data(ctx_id="ctx_924547")

    # choose item to change
    item = ctx.records[0]

    # change title (string strip)
    title = extract.title_from_item(item)
    title = title.strip()
    item['data']['metadata']['title'] = title

    # get identifier from item
    identifier = extract.idx_from_item(item)

    # comment on the changes
    comment = 'delete unnecessary white space'

    # update data in repository
    cl_auth.update_data(identifier, item['data'], comment)

    # to change values in collection of items use inspector class
    from pybman import Inspector
    from pybman import DataSet

    # create data set of released items
    ctx_released = DataSet(data_id="ctx_924547_released", raw=ctx.get_items_released())

    # create inspector instance of all released items from context
    inspector = Inspector(cl_auth, ctx_released.records)

    # strip title strings, i.e. remove leading and trailing white spaces
    titles = inspector.clean_titles()
    print("successfully cleaned", titles, "titles!")
