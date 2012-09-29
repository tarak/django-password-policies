from django.contrib.auth.models import User
from django.utils.encoding import force_unicode

from password_policies.tests.lib import BaseTest
from password_policies.forms import PasswordPoliciesForm, PasswordPoliciesChangeForm
from password_policies.forms.fields import PasswordPoliciesField


class PasswordPoliciesFieldTest(BaseTest):

    fixtures = ['django_password_policies_test_forms_fixtures.json']

    def test_password_field_1(self):
        self.assertFieldOutput(PasswordPoliciesField,
           {'Chad+pher9k': 'Chad+pher9k'},
           {
            'EUAdEHI3ES': [u'The new password must contain 1 or more symbol.'],
            })

    def test_password_field_2(self):
        self.assertFieldOutput(PasswordPoliciesField,
           {'Chad+pher9k': 'Chad+pher9k'},
           {
            u'4+53795': [u'The new password must contain 3 or more letters.'],
            })

    def test_password_field_3(self):
        self.assertFieldOutput(PasswordPoliciesField,
           {'Chad+pher9k': 'Chad+pher9k'},
           {
            u'Chad+pherg': [u'The new password must contain 1 or more number.'],
            })

    def test_password_field_4(self):
        self.assertFieldOutput(PasswordPoliciesField,
           {'Chad+pher9k': 'Chad+pher9k'},
           {
            u'aaaa5+56dddddd': [u'The new password contains consecutive characters. Only 3 consecutive characters are allowed.',
                                u'The new password is not varied enough.'],
            })

    def test_password_field_5(self):
        self.assertFieldOutput(PasswordPoliciesField,
           {'Chad+pher9k': 'Chad+pher9k'},
           {
            u'someone2@example.com': [u'The new password is not varied enough.',
                                      u'The new password is similar to an email address.'],
            })

    def test_password_field_6(self):
        self.assertFieldOutput(PasswordPoliciesField,
           {u'Ch\xc4d+pher9k': u'Ch\xc4d+pher9k'},
           {
            u'\xc1\xc2\xc3\xc4\u0662\xc5\xc6': [u'The new password must contain 1 or more symbol.'],
            })

    def test_password_field_7(self):
        self.assertFieldOutput(PasswordPoliciesField,
           {u'Ch\xc4d+pher9k': u'Ch\xc4d+pher9k'},
           {
            u'\xc1\xc2\xc3\xc4\u0662\xc5\u20ac': [u'Ensure this value has at least 8 characters (it has 7).'],
            },
            field_kwargs={'min_length':8})


class PasswordPoliciesFormTest(BaseTest):

    fixtures = ['django_password_policies_test_forms_fixtures.json']

    def test_reused_password(self):
        user = User.objects.get(username='alice')
        data = {
            'new_password1': 'K9hrfQH!zdj',
            'new_password2': 'K9hrfQH!zdj',
            }
        form = PasswordPoliciesForm(user, data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form["new_password1"].errors,
                         [force_unicode(form.error_messages['password_used'])])

    def test_password_mismatch(self):
        user = User.objects.get(username='alice')
        data = {
            'new_password1': 'Chah+pher9k',
            'new_password2': 'Chah+pher8k',
            }
        form = PasswordPoliciesForm(user, data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form["new_password2"].errors,
                         [force_unicode(form.error_messages['password_mismatch'])])

    def test_password_verification_unicode(self):
        user = User.objects.get(username='alice')
        password = u'\xc1\u20ac\xc3\xc4\u0662\xc5\xc6\xc7'
        self.assertEqual(len(password), 8)
        data = {
            'new_password1': password,
            'new_password2': password,
            }
        form = PasswordPoliciesForm(user, data)
        self.assertTrue(form.is_valid())

    def test_success(self):
        user = User.objects.get(username='alice')
        data = {
            'new_password1': 'Chah+pher9k',
            'new_password2': 'Chah+pher9k',
            }
        form = PasswordPoliciesForm(user, data)
        self.assertTrue(form.is_valid())


class PasswordPoliciesChangeFormTest(BaseTest):

    fixtures = ['django_password_policies_test_forms_fixtures.json']

    def test_password_invalid(self):
        user = User.objects.get(username='alice')
        data = {
            'old_password': 'Oor0ohf4bi',
            'new_password1': 'Chah+pher9k',
            'new_password2': 'Chah+pher9k',
            }
        form = PasswordPoliciesChangeForm(user, data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form["old_password"].errors,
                         [force_unicode(form.error_messages['password_incorrect'])])
        self.assertFalse(form.is_valid())

    def test_success(self):
        user = User.objects.get(username='alice')
        data = {
            'old_password': 'Oor0ohf4bi-',
            'new_password1': 'Chah+pher9k',
            'new_password2': 'Chah+pher9k',
            }
        form = PasswordPoliciesChangeForm(user, data)
        self.assertTrue(form.is_valid())
