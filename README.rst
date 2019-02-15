Pybman (*work in progress*)
=============================

Synopsis
--------

This is a python3 package (under development) for interacting with `MPG.PuRe <https://pure.mpg.de>`_ via the `PubMan REST API <https://pure.mpg.de/rest/swagger-ui.html>`_.


Usage
-----

For a preview install the package via ``pip`` and then in the python console::

    from pybman import Pybman
    # choose a context by id
    ctx_id = 'ctx_924547'
    # create pybman instance
    pyb = Pybman(ctx_id=ctx_id)
    # check out retrieved data
    example = pyb.ctx_data.records[0]
    print(example['data']['metadata'])
