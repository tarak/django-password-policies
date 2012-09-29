.. _setup:

==========================
Setting up the application
==========================

.. _setup-templates:

Required templates
==================

To use :ref:`the views in django-password-policies <api-views>` the same
templates used by the views in :mod:`django.contrib.auth` can be used,
except the templates to send the password reset email.

.. note::
  Because ``django-password-policies`` is intended to be highly reusable it does
  not include any other templates than the ones used for testing the 
  application. It is left to programmers using ``django-password-policies`` to
  create templates for projects as needed.

* ``registration/password_change_done.html``
    Used in the view :view:`PasswordChangeDoneView`.
    
    Displays a message that a password change has been completed
    successfully. Has no context variables.
* ``registration/password_change_form.html``
    Used in the view :view:`PasswordChangeFormView`.
    
    Displays the form to change a password. Has the following context variables:
    
    + ``form``
        The form used to change the user's password.
    + ``next``
        If a password change is forced the view will remember the URL the user
        wanted to visit before being redirect to this view.
        By default, the path that the user should be redirected to upon
        successful password change is stored in a query string parameter called
        "next".
        
        Note that if you provide a value to ``redirect_field_name``, you will most
        likely need to customize your login template as well, since the template
        context variable which stores the redirect path will use the value of
        ``redirect_field_name`` as its key rather than "next" (the default).

* ``registration/password_reset_complete.html``
    Used in the view :view:`PasswordResetCompleteView`.
    
    Displays a message that a password reset has been completed
    successfully. Has the following context variables:
    
    + ``login_url``
        The URL of the login page.

* ``registration/password_reset_confirm.html``
    Used in the view :view:`PasswordResetConfirmView`.
    
    Displays the form to reset a password. Has the following context variables:
    
    + ``form``
        The form used to reset the user's password.

* ``registration/password_reset_done.html``
    Used in the view :view:`PasswordResetDoneView`.
    
    Displays a message that a password reset has been started and that an email
    with instructions has been sent to the user. Has no context variables.
* ``registration/password_reset_email.html``
    Used in the form :form:`PasswordResetForm` to send the password reset email.
    
    This template is used to generate an HTML-attachment for the email. Has the
    following context variables:
    
    + ``domain``
        The domain name.
    + ``site_name``
        The name of the site.
    + ``protocol``
        The HTTP protocol. Either ``http`` or ``https``.
    + ``email``
        The user's email address.
    + ``signature``
        The signature token to use in a one-time secret URL.
    + ``timestamp``
        The timestamp token to use in a one-time secret URL.
    + ``uid``
        A base36-encoded string representig the user id.
    + ``user``
        The user instance.
    + ``request``
        The instance of the ``request``.

* ``registration/password_reset_email.txt``
    Used in the form :form:`PasswordResetForm` to send the password reset email.
    
    This template is used to generate the message body of the email. Has the
    following context variables:
    
    + ``domain``
        The domain name.
    + ``site_name``
        The name of the site.
    + ``protocol``
        The HTTP protocol. Either ``http`` or ``https``.
    + ``email``
        The user's email address.
    + ``signature``
        The signature token to use in a one-time secret URL.
    + ``timestamp``
        The timestamp token to use in a one-time secret URL.
    + ``uid``
        A base36-encoded string representig the user id.
    + ``user``
        The user instance.
    + ``request``
        The instance of the ``request``.

* ``registration/password_reset_form.html``
    Used in the view :view:`PasswordResetFormView`.
    
    Displays the form to start a password reset. Has the following context
    variables:
    
    * ``form``
        The form used to identify the user  by his/her email address.
* ``registration/password_reset_subject.txt``
    Used in the form :form:`PasswordResetForm` to send the password reset email.
    
    This template is used to generate the subject of the email. Has the
    following context variables:
    
    + ``domain``
        The domain name.
    + ``site_name``
        The name of the site.
    + ``protocol``
        The HTTP protocol. Either ``http`` or ``https``.
    + ``email``
        The user's email address.
    + ``signature``
        The signature token to use in a one-time secret URL.
    + ``timestamp``
        The timestamp token to use in a one-time secret URL.
    + ``uid``
        A base36-encoded string representig the user id.
    + ``user``
        The user instance.
    + ``request``
        The instance of the ``request``.

.. note::
  Minimal example templates can be found inside the tests module of
  ``django-password-policies``.

.. _setup-urls:

Setting up URLs
===============

``django-password-policies`` includes a Django ``URLconf`` which sets up URL patterns
for :ref:`the views in django-password-policies <api-views>`. This ``URLconf`` can be
found at ``password_policies.urls``, and so can simply be included in a project's
root URL configuration. For example, to place the URLs under the prefix
``/password/``, one could add the following to a project's root ``URLconf``::

    (r'^password/', include('password_policies.urls')),

Users would then be able to change their password by visiting the URL
``/password/change/`` or to reset their password by visiting the URL
``/password/reset/``.

.. _setup-add-to-apps:

Adding the app to the installed applications
============================================

To use ``django-password-policies`` in a Django project add ``password_policies`` to the
``INSTALLED_APPS`` setting of a project.

For example, one might have something like the following in a Django settings
file::

    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.admin',
        'django.contrib.messages',
        'password_policies',
        # ...other installed applications...
    )

.. _setup-create-db-tables:

Creating the database tables
============================

To create the database tables needed by ``django-password-policies`` simply run
the following inside a project's root directory::

    $ python manage.py syncdb

