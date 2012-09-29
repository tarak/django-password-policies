.. _contributing:

============
Contributing
============

``django-password-policies`` is an open source project managed using the Git
version control system. The repository is hosted on `GitHub`_, so contributing
is as easy as forking the project and committing back your enhancements.

Please note the following guidelines for contributing:

* Contributed code must be written in the existing style. This is
  as simple as following the `Django coding style`_ and (most
  importantly) `PEP 8`_.
* Contributions must be available on a separately named branch
  based on the latest version of the main branch.
* Run the tests before committing your changes. If your changes
  cause the tests to break, they won't be accepted.
* If you are adding new functionality, you must include basic tests
  and documentation.
* If you write tests you should use the included BaseTest and use test
  fixtures::
    
    from password_policies.tests.lib import BaseTest
    
    class CustomTest(BaseTest):

        fixtures = ['django_password_policies_custom_fixtures.json']

        def test_something(self):
            pass
        
* Documentation must be formatted to be used with `Sphinx`_.

.. _`PEP 8`: http://www.python.org/dev/peps/pep-0008/
.. _`Django coding style`: http://docs.djangoproject.com/en/dev/internals/contributing/#coding-style
.. _`GitHub`: https://github.com/tarak/django-password-policies/
.. _`Sphinx`: http://sphinx.pocoo.org/
