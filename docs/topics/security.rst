.. _security:

========
Security
========

.. _notes:

--------------------
Notes about security
--------------------

The use of a security related application like this one implies consequences.
The following notes should be read carefully to understand how this application
works:

* When a user changes his/her password, and only then, the old password is
  compared to the new using the Levenshtein algorithm. This of course doesn't
  work doing a password reset, obviously because the user has forgotten the old
  password.

* This application only counts letters, numbers and symbols in passwords. It
  does not try to differentiate between upper- or lowercase letter, simply
  because there are languages without uppercase letters. Forcing users speaking
  only these languages to use characters of "foreign" scripts is not really
  user friendly. The usage of unicode characters and especially numbers and
  symbols makes it hard enough to crack such a password.
  
* The minimum length of a password is the required number of letters, numbers
  and symbols. The :class:`~password_policies.forms.fields.PasswordPoliciesField` uses
  the :attr:`min_length` attribute, but the usage only makes sense if you want
  to, in example, enforce 3 letters, 1 number and 1 symbol in a password with
  a minimum length of 8 characters, which is the default, by the way...
  
* The maximum length for a password is not limited by default, but can easyily
  be set using :ref:`api-settings`.

* Using the dictionary validator is basically opening a text file with a single
  word per line, reading ALL lines into memory and perform validation.
  
  The same applies to the list of words specific to each project.
  
  This slows down the validator depending of the sizes of lines or list entries.
  
  Also note that the validator opens the text file each time it is called.
  
  Therefor the validator is disabled by default, but can easily be enabled in
  each projects :ref:`api-settings`.

* The validator using the `Python bindings for cracklib`_ does not handle
  unicode characters and is disabled by default. Considering the advantage of
  such a validator, it was included in this application anyway. Like the
  dictionary validator it is disabled by default, but can easily be enabled in
  each projects :ref:`api-settings`.

* The password history, if enabled, stores the user's password by generating a
  newly encrypted version of the new password, each time a user changes his/her
  password, using the included ``django-password-policies`` forms. Django
  includes a mechanism to compare a raw password with different encrypted
  passwords. No unencrypted password is saved to the database!

.. _`Python bindings for cracklib`: http://www.nongnu.org/python-crack/
