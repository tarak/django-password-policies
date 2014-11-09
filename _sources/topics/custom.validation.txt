.. _custom-validation:

======================
Customizing validation
======================

.. _built-in-validators:

-----------------------------
Using the built-in validators
-----------------------------

The built-in validators can be customized by changing values in a project's
settings file.

A list of built-in validators is available at:

* :ref:`api-validators`

A list of default application settings is available at:

* :ref:`api-settings`

.. _custom-use:

---------------------------------
Customizing by sub-classing forms
---------------------------------

Customizing password validation can be used by simply using a
:formfield:`PasswordPoliciesField` and :form:`PasswordPoliciesForm`::

    from password_policies.conf import settings
    from password_policies.forms import PasswordPoliciesForm
    from password_policies.forms.fields import PasswordPoliciesField

    from your_app import your_custom_validators


    class CustomPasswordPoliciesForm(PasswordPoliciesForm):
        """
    A form that lets a user set his/her password without entering the
    old password.
    """
        new_password1 = PasswordPoliciesField(label=_("New password"),
            max_length=settings.PASSWORD_MAX_LENGTH,
            min_length=settings.PASSWORD_MIN_LENGTH,
            validators=[your_custom_validators.some_validator,
                        your_custom_validators.another_validator],)

        def clean(self):
            cleaned_data = super(CustomPasswordPoliciesForm, self).clean()
            new_password1 = cleaned_data.get("new_password1")
            new_password2 = cleaned_data.get("new_password2")

            if new_password1 and new_password2:
                # Perform additional validation...
                pass

            # Always return the full collection of cleaned data.
            return cleaned_data

To use the form with the built-in :view:`PasswordResetConfirmView` an
URL pattern needs to be added to a project's ``URLconf``::


    from password_policies.views import PasswordResetConfirmView

    from your_app.forms import CustomPasswordPoliciesForm

    urlpatterns = patterns('',
        (r'^password/reset/', PasswordResetConfirmView.as_view(form_class=CustomPasswordPoliciesForm)),
    )
