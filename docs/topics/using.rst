.. _using:

=====================
Using the application
=====================

``django-password-policies`` uses settings to control different customizable aspects
of the application. Here is a list of available application settings:

.. _settings:

------------------
Available settings
------------------

.. setting:: EMAIL_CHANGE_DELETE_SUCCESS_REDIRECT_URL

``EMAIL_CHANGE_DELETE_SUCCESS_REDIRECT_URL``
--------------------------------------------

Default: ``'/account/email/change/'``

Determines the URL to redirect to after a pending email address change request
has been deleted.

.. setting:: EMAIL_CHANGE_FROM_EMAIL

``EMAIL_CHANGE_FROM_EMAIL``
---------------------------

Default: ``django.conf.settings.DEFAULT_FROM_EMAIL``

Determines the email address to use as sender of confirmation mails.

.. setting:: EMAIL_CHANGE_HTML_EMAIL

``EMAIL_CHANGE_HTML_EMAIL``
---------------------------

Default: ``False``

Determines wether to send confirmation mails with HTML-attachments.

.. setting:: EMAIL_CHANGE_HTML_EMAIL_TEMPLATE

``EMAIL_CHANGE_HTML_EMAIL_TEMPLATE``
------------------------------------

Default: ``'change_email/mail/body.html'``

The template to use for HTML-formatted emails. Technically an attachment to the
confirmation mail with mimetype 'text/html'.

.. note::
  The template is not rendered and attached to the mail if :setting:`EMAIL_CHANGE_HTML_EMAIL` is set to `False`.

.. setting:: EMAIL_CHANGE_SUBJECT_EMAIL_TEMPLATE

``EMAIL_CHANGE_SUBJECT_EMAIL_TEMPLATE``
---------------------------------------

Default: ``'change_email/mail/subject.txt'``

The template to use for the subject of the confirmation mail.

.. note::
  Because this template is used as the subject line of an email, the template’s
  output must be only a single line of text; output that contains newlines will
  be forcibly joined into only one single line.
  Also note that the template's content should be put into an ``autoescape``-
  tag with ``off`` as argument.

.. setting:: EMAIL_CHANGE_TIMEOUT

``EMAIL_CHANGE_TIMEOUT``
-----------------------------

Default: ``60*60*24*7 (7 days)``

Determines after how many seconds pending email address change requests expire.

.. setting:: EMAIL_CHANGE_TXT_EMAIL_TEMPLATE

``EMAIL_CHANGE_TXT_EMAIL_TEMPLATE``
-----------------------------------

Default: ``'change_email/mail/body.txt'``

The template to use for the mail body. Technically just plain text.

.. note::
  The template's content should be put into an ``autoescape``-tag with ``off``
  as argument.
  
.. _maintenance:

-----------
Maintenance
-----------

``django-password-policies`` provides a maintenance command to delete expired email
address change requests automatically. To do so, simply run the following inside
a project's root directory::

    $ python manage.py cleanupemailchangerequests
