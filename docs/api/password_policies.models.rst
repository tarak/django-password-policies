.. _api-models:

Models
======

.. automodule:: password_policies.models


.. model:: PasswordHistory

``PasswordHistory``
-------------------

.. autoclass:: password_policies.models.PasswordHistory
   :members:

   .. attribute:: password

       Required. The encrypted password.

   .. attribute:: user

       Required. The :class:`~django.contrib.auth.models.User`.

   .. attribute:: created

       A :py:obj:`.datetime` of the request's creation. Is set to the current
       date/time upon instance creation.

