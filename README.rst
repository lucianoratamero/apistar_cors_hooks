apistar_cors_hooks
==================

.. image:: https://travis-ci.org/lucianoratamero/apistar_cors_hooks.svg?branch=master
    :target: https://travis-ci.org/lucianoratamero/apistar_cors_hooks

This project enables CORS on `API Star`_\  apps via event hooks.

Suppports:

- apistar>=0.4.0
- python>=3.6

Installation
~~~~~~~~~~~~

Install via PyPI:

.. code:: shell

    pip install apistar_cors_hooks


After installing, we need to add and instance of ``CORSRequestHooks`` to your ``event_hooks`` in your app:

.. code:: python

    from apistar import App, Route
    from apistar_cors_hooks import CORSRequestHooks


    def homepage() -> str:
        return '<html><body><h1>Homepage</h1></body></html>'


    routes = [
        Route('/', method='GET', handler=homepage),
    ]

    event_hooks = [CORSRequestHooks()]
    app = App(routes=routes, event_hooks=event_hooks)

If you want to customize WSGICORS options, you just need to pass a dict via the ``options`` kwarg:

.. code:: python

    custom_options = {"origin": "your_host_server"}
    event_hooks = [CORSRequestHooks(options=custom_options)]
    app = App(routes=routes, event_hooks=event_hooks)


Contributing
~~~~~~~~~~~~

Since I'm a WSGI/CORS noob, I may have left a bug or two, or didn't think of better ways to implement this.

Be free to open an issue, contribute with PRs and contact me at ``luciano@ratamero.com``.

.. _API Star: https://github.com/encode/apistar


Changelog
~~~~~~~~~~~~

0.1.0
'''''
- initial version
