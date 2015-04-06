from django import forms

from password_policies.forms.validators import validate_common_sequences
from password_policies.forms.validators import validate_consecutive_count
from password_policies.forms.validators import validate_cracklib
from password_policies.forms.validators import validate_dictionary_words
from password_policies.forms.validators import validate_entropy
from password_policies.forms.validators import validate_letter_count
from password_policies.forms.validators import validate_number_count
from password_policies.forms.validators import validate_symbol_count
from password_policies.forms.validators import validate_not_email


class PasswordPoliciesField(forms.CharField):
    """
A form field that validates a password using :ref:`api-validators`.
"""
    default_validators = [validate_common_sequences,
                          validate_consecutive_count,
                          validate_cracklib,
                          validate_dictionary_words,
                          validate_letter_count,
                          validate_number_count,
                          validate_symbol_count,
                          validate_entropy,
                          validate_not_email]

    def __init__(self, *args, **kwargs):
        if "widget" not in kwargs:
            kwargs["widget"] = forms.PasswordInput(render_value=False)
        super(PasswordPoliciesField, self).__init__(*args, **kwargs)
