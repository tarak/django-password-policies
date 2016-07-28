.. _install:

============
Installation
============

.. _install-requirements:

Requirements
============

This application requires

* `Django`_ 1.7 or newer
* `django-easysettings`_

.. _install-cracklib:

Cracklib
========

To use the included :class:`~password_policies.forms.validators.CracklibValidator`
the `Python bindings for cracklib`_ need to be installed.

.. warning::
    The :class:`~password_policies.forms.validators.CracklibValidator` is not
    used if the crack module is not installed.

On most linux distros it can simply be installed via a package manager. On
Debian based distributions the according package is called:

* python-cracklib

.. _install-levenshtein:

Levenshtein
===========

The included :class:`~password_policies.forms.PasswordPoliciesChangeForm` uses
the `Levenshtein Python C extension module`_.

.. warning::
    The :class:`~password_policies.forms.PasswordPoliciesChangeForm` does not
    compare both the old and new password if the module is not installed.

On most linux distros it can simply be installed via a package manager. On
Debian based distributions the according package is called:

* python-levenshtein

.. _install-pypi:

From Pypi
=========

To install from `PyPi`_::

    [sudo] pip install django-password-policies

or::

    [sudo] easy_install django-password-policies

.. _`PyPi`: https://pypi.python.org/pypi/django-password-policies

.. _install-source:

From source
===========

The latest release package can be downloaded from `the GitHub download page`_.

.. _`the GitHub download page`: https://github.com/tarak/django-password-policies/releases

Once you've downloaded the package, unpack it (on most operating systems, simply
double-click; alternately, at a command line on Linux, Mac OS X or other
Unix-like systems, type)::

    $ tar zxvf django-password-policies-<VERSION>.tar.gz

This will create the directory::

    django-password-policies-<VERSION>

which contains
the ``setup.py`` installation script. From a command line in that directory,
type::

    python setup.py install

Note that on some systems you may need to execute this with
administrative privileges (e.g., ``sudo python setup.py install``).

Another possibility to install the application is to create a link to the app
inside the Python path::

    $ sudo ln -s django-password-policies/password_policies /path/to/python_site_packages/password_policies


.. _`Django`: https://www.djangoproject.com/
.. _`django-easysettings`: https://github.com/SmileyChris/django-easysettings
.. _`Python bindings for cracklib`: http://www.nongnu.org/python-crack/
.. _`Levenshtein Python C extension module`: https://github.com/miohtama/python-Levenshtein
