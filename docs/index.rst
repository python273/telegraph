Python telegraph module
=======================

Installation
------------

.. code-block:: shell-session

    $ python3 -m pip install telegraph
    # with asyncio support
    $ python3 -m pip install 'telegraph[aio]'

Example
-------

.. code-block:: python

    from telegraph import Telegraph

    telegraph = Telegraph()
    telegraph.create_account(short_name='1337')

    response = telegraph.create_page(
        'Hey',
        html_content='<p>Hello, world!</p>'
    )
    print(response['url'])

Async Example
-------------

.. code-block:: python

    import asyncio
    from telegraph.aio import Telegraph

    async def main():
        telegraph = Telegraph()
        print(await telegraph.create_account(short_name='1337'))

        response = await telegraph.create_page(
            'Hey',
            html_content='<p>Hello, world!</p>',
        )
        print(response['url'])


    asyncio.run(main())


.. toctree::
    :maxdepth: 4
    :caption: Contents:

    telegraph


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
