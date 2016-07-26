#!/usr/bin/env python
#!/usr/bin/env python
import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner


def runtests(*test_args):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'password_policies.tests.settings'
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(["tests"])
    sys.exit(bool(failures))


if __name__ == '__main__':
    runtests(*sys.argv[1:])
