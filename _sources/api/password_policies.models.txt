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

       Required. The new email address.

   .. attribute:: user

       Required. The :class:`~django.contrib.auth.models.User` that has
       requested the change of email address. Must be set by the view creating
       an email address change request.

   .. attribute:: created

       A :py:obj:`.datetime` of the request's creation. Is set to the current
       date/time upon instance creation.

