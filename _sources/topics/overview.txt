.. _overview:

========
Overview
========

.. _features:

--------
Features
--------

``django-password-policies`` is an application for the `Django`_ framework that

* provides a form field and forms that handle the validation of
  unicode passwords using different validators, see :ref:`api-validators`.

* checks that passwords containing unicode characters conform to `RFC 4013`_,
  including checks for

  - bidirectional characters and
  - invalid unicode characters.

* verifies if passwords contain

  - consecutive repetitions of the same characters,
  - common sequences,
  - dictionary words, using

    + `Python bindings for cracklib`_,
    + a custom dictionary
    + and a list of words specific to each project.

* verifies that a new password is not too similar to an old one when a user
  changes his/her password.

* verifies that a new password is not equal to an email address.

* implements a password history for users making it possible to check if users
  try to use passwords again.

* uses `Django`_'s cryptographic signing API to generate one-time secret URLs
  for password resets.

.. _`Django`: https://www.djangoproject.com/
.. _`RFC 4013`: http://tools.ietf.org/html/rfc4013
.. _`Python bindings for cracklib`: http://www.nongnu.org/python-crack/
