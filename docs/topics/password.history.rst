.. _password-history:

==========================
Using the password history
==========================

``django-password-policies`` provides a password history to "remember" user
passwords. To deactivate the password history for a project the following needs
to be added to a project's settings file::

    # Defaults to True
    PASSWORD_USE_HISTORY = False

To customize how many passwords are saved in a user's password history the
following setting can be set::

    # Defaults to 10
    PASSWORD_HISTORY_COUNT = 20

Each time a user changes his/her password it is counted how many entries in a
user's password history exist. If there a more than
:py:attr:`~password_policies.conf.Settings.PASSWORD_HISTORY_COUNT` older entries
are deleted automatically from the user's password history upon successfull
password change.
