"""
Unit tests runner for ``django-change-email``.
Setuptools needs instructions how to interpret
``test`` command when we run::

    python setup.py test

"""
import os
import sys
import django

os.environ["DJANGO_SETTINGS_MODULE"] = 'password_policies.tests.settings'
from password_policies.tests import settings

settings.DJALOG_LEVEL = 40
settings.INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.contenttypes',
    'django.contrib.admin',
    'django.contrib.sites',
    'password_policies',
)

def run_tests(settings):
    from django.test.utils import get_runner
    from django.utils.termcolors import colorize
    from django.test.utils import setup_test_environment
    version = django.get_version()
    if version.startswith("1.7"):
        django.setup()
    db_conf = settings.DATABASES['default']
    setup_test_environment()
    output = []
    msg = "Starting tests for db backend: %s" % db_conf['ENGINE']
    embracer = '=' * len(msg)
    output.append(msg)
    for key, value in db_conf.iteritems():
        if key == 'PASSWORD':
            value = '****************'
        line = '    %s: "%s"' % (key, value)
        output.append(line)
    embracer = colorize('=' * len(max(output, key=lambda s: len(s))),
        fg='green', opts=['bold'])
    output = [colorize(line, fg='blue') for line in output]
    output.insert(0, embracer)
    output.append(embracer)
    print '\n'.join(output)

    TestRunner = get_runner(settings)
    test_runner = TestRunner(interactive=False)
    failures = test_runner.run_tests(['password_policies'])
    return failures

def main():
    failures = run_tests(settings)
    sys.exit(failures)

if __name__ == '__main__':
    main()
