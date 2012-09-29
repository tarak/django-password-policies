.. _forced-password-changes:

========================
Forcing password changes
========================

.. note::
    Forcing password changes only works if
    the :doc:`password history <password.history>` is activated.

``django-password-policies`` provides the possibility to force password resets
when user passwords expire. To activate forced password changes for a project
different settings need to be set:

.. _password-change-requirements:

------------
Requirements
------------

To use the password change feature Django's authentication and sessions
framework is used. It must be set up correctly for the middleware and the
context processor to work::

    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'password_policies',
    )

For more informations on the authentication and sessions framework please
consult the `Django documentation`_.

.. _password-change-expiry:

-----------------------
Setting password expiry
-----------------------

To customize the duration of a password the following setting can be added to a
project's settings file::
    
    # Defaults to 60 days.
    PASSWORD_DURATION_SECONDS = 24 * 60**3

.. _password-change-middleware:

--------------------
Using the middleware
--------------------

Forcing password changes is done using the
:middleware:`PasswordChangeMiddleware`. To use it add it to the list of
``MIDDLEWARE_CLASSES`` in a project's settings file::

    MIDDLEWARE_CLASSES = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'password_policies.middleware.PasswordChangeMiddleware',
        # ... other middlewares ...
    )

.. note::
    The order of this middleware in the stack is important,
    it must be listed after the authentication AND the session
    middlewares.

.. _password-change-context-processor:

---------------------------
Using the context processor
---------------------------

``django-password-policies`` provides a context processor that adds a template
variable to the context. To use it add it to the list of
``TEMPLATE_CONTEXT_PROCESSORS`` in a project's settings file::

    TEMPLATE_CONTEXT_PROCESSORS = (
        'django.contrib.auth.context_processors.auth',
        'django.core.context_processors.debug',
        'django.core.context_processors.i18n',
        'django.contrib.messages.context_processors.messages',
        'password_policies.context_processors.password_status',
    )

Then the template for the password change view can display a message if the user
is required to change his/her password::

    {% extends 'registration/base.html' %}
    {% load i18n %}
    {% if password_change_required %}
    <p class='help'>{% trans "Your password has expired. Please change it using the form below." %}</p>
    {% endif %}
    <form action="." method="post">{% csrf_token %}
    {{ form.as_p }}{% if next %}
    <input type="hidden" name="next" value="{{ next }}" />{% endif %}
    <input type="submit" value="Submit" />
    </form>

.. _`Django documentation`: https://docs.djangoproject.com/en/dev/
