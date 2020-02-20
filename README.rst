=============================================
 The :mod:`nectarallocationclient` Python API
=============================================

.. module:: nectarallocationclient
   :synopsis: A client for the Nectar Allocation API.

.. currentmodule:: nectarallocationclient

Usage
-----

First create a client instance using the keystoneauth session API::

    >>> from keystoneauth1 import loading
    >>> from keystoneauth1 import session
    >>> from nectarallocationclient import client
    >>> loader = loading.get_plugin_loader('password')
    >>> auth = loader.load_from_options(auth_url=AUTH_URL,
    ...                                 username=USERNAME,
    ...                                 password=PASSWORD,
    ...                                 project_name=PROJECT_NAME,
    ...                                 user_domain_id='default',
    ...                                 project_domain_id='default'
    )
    >>> sess = session.Session(auth=auth)
    >>> nectar = client.Client(VERSION, session=sess)

Here ``VERSION`` can currently only be ``1``.

If you have PROJECT_ID instead of a PROJECT_NAME, use the project_id
parameter. Similarly, if your cloud uses keystone v3 and you have a DOMAIN_NAME
or DOMAIN_ID, provide it as `user_domain_(name|id)` and if you are using a
PROJECT_NAME also provide the domain information as `project_domain_(name|id)`.

nectarallocationclient adds 'python-nectarallocationclient' and its version to the user-agent string
that keystoneauth produces. If you are creating an application using nectarallocationclient
and want to register a name and version in the user-agent string, pass those
to the Session::

    >>> sess = session.Session(
    ...     auth=auth, app_name'nodepool', app_version'1.2.3')

If you are making a library that consumes nectarallocationclient but is not an end-user
application, you can append a (name, version) tuple to the session's
`additional_user_agent` property::

    >>> sess = session.Session(auth=auth)
    >>> sess.additional_user_agent.append(('shade', '1.2.3'))

For more information on this keystoneauth API, see `Using Sessions`_.

.. _Using Sessions: https://docs.openstack.org/keystoneauth/latest/using-sessions.html


Then call methods on its managers::

    >>> nectar.allocations.list()
    [<Allocation: 1 (my-cool-project)>]

    >>> nectar.allocations.create("new-project",....)
    <Allocation: 2 (new-project)>

