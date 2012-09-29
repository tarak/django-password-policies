.. _api-forms:

Forms
=====

``django-password-policies`` ships two :class:`django.forms.Form` classes that
handles the validation of new passwords:

.. automodule:: password_policies.forms

.. form:: PasswordPoliciesForm

``PasswordPoliciesForm``
------------------------

.. autoclass:: password_policies.forms.PasswordPoliciesForm
   :members:
   :special-members:

   .. attribute:: new_password1
   
       The new password.
       
       Required. A :class:`~password_policies.forms.fields.PasswordPoliciesField`.

   .. attribute:: new_password2
   
       The new password,
       to confirm that it was given in correctly.
       
       Required. A :class:`~django.forms.CharField` with
       a :class:`~django.forms.PasswordInput` widget.

.. form:: PasswordPoliciesChangeForm

``PasswordPoliciesChangeForm``
------------------------------

.. autoclass:: password_policies.forms.PasswordPoliciesChangeForm
   :members:
   :show-inheritance:

   .. attribute:: old_password
   
       The actual password.
       
       Required. A :class:`~django.forms.CharField` with
       a :class:`~django.forms.PasswordInput` widget.

.. form:: PasswordPoliciesRegistrationForm

``PasswordPoliciesRegistrationForm``
------------------------------------

.. autoclass:: password_policies.forms.PasswordPoliciesRegistrationForm
   :members:
   :special-members:

   .. attribute:: username
   
       The username that the user wants to register.
       
       Required. A :class:`~django.forms.CharField`.

   .. attribute:: password1
   
       The new password.
       
       Required. A :class:`~password_policies.forms.fields.PasswordPoliciesField`.

   .. attribute:: password2
   
       The new password,
       to confirm that it was given in correctly.
       
       Required. A :class:`~django.forms.CharField` with
       a :class:`~django.forms.PasswordInput` widget.

.. form:: PasswordResetForm

``PasswordResetForm``
------------------------------

.. autoclass:: password_policies.forms.PasswordResetForm
   :members:

   .. attribute:: email
   
       The actual email address of a user.
       
       Required. A :class:`~django.forms.EmailField`.
