from django.core.urlresolvers import reverse

from password_policies.forms import PasswordPoliciesChangeForm
from password_policies.models import PasswordHistory
from password_policies.tests.lib import BaseTest
from password_policies.tests.lib import create_user
from password_policies.tests.lib import passwords


class PasswordChangeViewsTestCase(BaseTest):

    def setUp(self):
        self.user = create_user()
        return super(PasswordChangeViewsTestCase, self).setUp()
        #

    def test_password_change(self):
        """
        A ``GET`` to the ``password_change`` view uses the appropriate
        template and populates the password change form into the context.
        """
        self.client.login(username='alice', password=passwords[-1])
        response = self.client.get(reverse('password_change'))
        self.assertEqual(response.status_code, 200)
        self.failUnless(isinstance(response.context['form'],
                                   PasswordPoliciesChangeForm))
        self.assertTemplateUsed(response,
                                'registration/password_change_form.html')
        self.client.logout()

    def test_password_change_failure(self):
        """
        A ``POST`` to the ``password_change`` view with invalid data properly
        fails and issues the according error.
        """
        data = {
            'old_password': 'password',
            'new_password1': 'Chah+pher9k',
            'new_password2': 'Chah+pher9k',
        }
        msg = "Your old password was entered incorrectly. Please enter it again."
        self.client.login(username='alice', password=passwords[-1])
        response = self.client.post(reverse('password_change'), data=data)
        self.assertEqual(response.status_code, 200)
        self.failIf(response.context['form'].is_valid())
        self.assertFormError(response, 'form', field='old_password',
                             errors=msg)
        self.client.logout()

    def test_password_change_success(self):
        """
        A ``POST`` to the ``change_email_create`` view with valid data properly
        changes the user's password, creates a new password history entry
        for the user and issues a redirect.
        """
        data = {'old_password': passwords[-1],
                'new_password1': 'Chah+pher9k',
                'new_password2': 'Chah+pher9k'}
        self.client.login(username='alice', password=data['old_password'])
        response = self.client.post(reverse('password_change'), data=data)
        self.assertEqual(PasswordHistory.objects.count(), 1)
        obj = PasswordHistory.objects.get()
        self.assertRedirects(response,
                             'http://testserver%s' % reverse('password_change_done'))
        obj.delete()
        self.client.logout()
