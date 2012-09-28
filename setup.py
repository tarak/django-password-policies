from setuptools import setup, find_packages

setup(
    name='password_policies',
    version=__import__('password_policies').__version__,
    description='A Django application to implent password policies.',
    long_description="""Yet to come""",
    author='Tarak Blah',
    author_email='halbkarat@gmail.com',
    url='https://github.com/tarak/django-password-policies',
    include_package_data=True,
    packages=find_packages(),
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    test_suite='tests.main',
)
