.. _api-validators:

Validators
==========

django-password-policies provides validators to check new passwords:

.. automodule:: password_policies.forms.validators

.. validator:: BaseCountValidator

``BaseCountValidator``
----------------------

.. autoclass:: password_policies.forms.validators.BaseCountValidator
   :members:
   :member-order: bysource

.. validator:: BaseRFC4013Validator

``BaseRFC4013Validator``
------------------------

.. autoclass:: password_policies.forms.validators.BaseRFC4013Validator
   :members:
   :member-order: bysource

.. validator:: BaseSimilarityValidator

``BaseSimilarityValidator``
---------------------------

.. autoclass:: password_policies.forms.validators.BaseSimilarityValidator
   :members:
   :member-order: bysource

.. validator:: BidirectionalValidator

``BidirectionalValidator``
------------------------------------

.. autoclass:: password_policies.forms.validators.BidirectionalValidator
   :members:
   :inherited-members:
   :show-inheritance:
   :member-order: bysource

.. validator:: CommonSequenceValidator

``CommonSequenceValidator``
---------------------------

.. autoclass:: password_policies.forms.validators.CommonSequenceValidator
   :members:
   :show-inheritance:
   :inherited-members:
   :member-order: bysource

.. validator:: ConsecutiveCountValidator

``ConsecutiveCountValidator``
-----------------------------

.. autoclass:: password_policies.forms.validators.ConsecutiveCountValidator
   :members:
   :member-order: bysource

.. validator:: CracklibValidator

``CracklibValidator``
---------------------

.. autoclass:: password_policies.forms.validators.CracklibValidator
   :members:
   :member-order: bysource

.. note::
    For additional informations please consult the
    `Python bindings for cracklib documentation`_.

.. validator:: DictionaryValidator

``DictionaryValidator``
-----------------------

.. autoclass:: password_policies.forms.validators.DictionaryValidator
   :members:
   :show-inheritance:
   :inherited-members:
   :member-order: bysource

.. validator:: EntropyValidator

``EntropyValidator``
--------------------

.. autoclass:: password_policies.forms.validators.EntropyValidator
   :members:
   :member-order: bysource

.. validator:: InvalidCharacterValidator

``InvalidCharacterValidator``
------------------------------

.. autoclass:: password_policies.forms.validators.InvalidCharacterValidator
   :members:
   :show-inheritance:
   :inherited-members:
   :member-order: bysource

.. validator:: LetterCountValidator

``LetterCountValidator``
------------------------

.. autoclass:: password_policies.forms.validators.LetterCountValidator
   :members:
   :show-inheritance:
   :inherited-members:
   :member-order: bysource

.. validator:: NotEmailValidator

``NotEmailValidator``
---------------------

.. autoclass:: password_policies.forms.validators.NotEmailValidator
   :members:
   :member-order: bysource

.. validator:: NumberCountValidator

``NumberCountValidator``
------------------------

.. autoclass:: password_policies.forms.validators.NumberCountValidator
   :members:
   :show-inheritance:
   :inherited-members:

.. validator:: SymbolCountValidator

``SymbolCountValidator``
------------------------

.. autoclass:: password_policies.forms.validators.SymbolCountValidator
   :members:
   :show-inheritance:
   :inherited-members:
   :member-order: bysource

.. validator:: validate_bidirectional

``validate_bidirectional``
--------------------------
.. data:: validate_bidirectional

    A :class:`BidirectionalValidator` instance.

.. validator:: validate_common_sequences

``validate_common_sequences``
-----------------------------
.. data:: validate_common_sequences

    A :class:`CommonSequenceValidator` instance.

.. validator:: validate_consecutive_count

``validate_consecutive_count``
------------------------------
.. data:: validate_consecutive_count

    A :class:`ConsecutiveCountValidator` instance.

.. validator:: validate_cracklib

``validate_cracklib``
---------------------
.. data:: validate_cracklib

    A :class:`CracklibValidator` instance.

.. validator:: validate_dictionary_words

``validate_dictionary_words``
-----------------------------
.. data:: validate_dictionary_words

    A :class:`DictionaryValidator` instance.

.. validator:: validate_entropy

``validate_entropy``
--------------------
.. data:: validate_entropy

    A :class:`EntropyValidator` instance.

.. validator:: validate_invalid_character

``validate_invalid_character``
------------------------------
.. data:: validate_invalid_character

    A :class:`InvalidCharacterValidator` instance.

.. validator:: validate_letter_count

``validate_letter_count``
-------------------------
.. data:: validate_letter_count

    A :class:`LetterCountValidator` instance.

.. validator:: validate_not_email

``validate_not_email``
----------------------
.. data:: validate_not_email

    A :class:`NotEmailValidator` instance.

.. validator:: validate_number_count

``validate_number_count``
-------------------------
.. data:: validate_number_count

    A :class:`NumberCountValidator` instance.

.. validator:: validate_symbol_count

``validate_symbol_count``
-------------------------
.. data:: validate_symbol_count

    A :class:`SymbolCountValidator` instance.

.. _`Python bindings for cracklib documentation`: http://www.nongnu.org/python-crack/doc/index.html
