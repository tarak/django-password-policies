from datetime import timedelta
from random import randint

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.test import TestCase

from password_policies.conf import settings
from password_policies.models import PasswordHistory


passwords = [
    'ohl"ahn8aiSu',
    'la]ePhae1Ies',
    'xareW&ang4sh',
    'haea_d7AiWoo',
    'Eim9Co:e0aev',
    'Ve2eereil>ai',
    'Aengae]t:ie4',
    'ao6Lei+Hip=u',
    'zo!i8aigai{L',
    'Ju8AhGhoo(p?',
    'xieY6fohv>ei',
    'Elu1ie*z5aa3',
    'ooDei1Hoo+Ru',
    'Xohth3ohpu$o',
    'ia)D5AP7sie$',
    'heeb8aeCh-ae'
]


class BaseTest(TestCase):

    def setUp(self):
        """
        Isolate all application specific settings.
        """
        output = super(BaseTest, self).setUp()
        settings.isolated = True
        return output

    def tearDown(self):
        """
        Restore settings to their original state.
        """
        settings.isolated = False
        settings.revert()
        return super(BaseTest, self).tearDown()


def create_user(username="alice", email="alice@example.com", raw_password=None,
                date_joined=None, last_login=None, commit=True):
    """ Creates a non-staff user with dynamically generated properties.
This function dynamically creates an user with following properties:
- The user is neither an admin nor a staff member.
- The user is active.
- The date and his/her last login is generated dynamically.
"""
    count = settings.PASSWORD_HISTORY_COUNT
    duration = settings.PASSWORD_DURATION_SECONDS
    if not raw_password:
        raw_password = passwords[-1]
    if not date_joined:
        rind = randint(0, (duration / count + 1))
        seconds = (count * duration + rind) * 2
        date_joined = get_datetime_from_delta(timezone.now(), seconds)
    if not last_login:
        last_login = date_joined
    user = get_user_model()(username=username, email=email, is_active=True, last_login=last_login, date_joined=date_joined)
    user.set_password(raw_password)
    if commit:
        user.save()
    return user


def create_password_history(user, password_list=[]):
    duration = settings.PASSWORD_DURATION_SECONDS
    if not password_list:
        password_list = passwords
    seconds = len(password_list) * duration
    created = get_datetime_from_delta(timezone.now(), seconds)
    for raw_password in password_list:
        password = make_password(raw_password)
        entry = PasswordHistory.objects.create(password=password, user=user)
        entry.created = created
        entry.save()
        created = get_datetime_from_delta(created, (duration * -1))


def get_datetime_from_delta(value, seconds):
    "Returns a Datetime value after subtracting given seconds."
    return value - timedelta(seconds=seconds)
