import os

from setuptools import find_packages, setup


README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name = 'postoffice_django',
    version = '0.3.0',
    packages=find_packages(exclude=("tests",)),
    include_package_data = True,
    license = 'APACHE License',
    description = 'A simple Django app to comunicate with post office',
    long_description = README,
    url = 'http://www.example.com/',
    author = 'Mercadona',
    author_email = 'sofware.online@mercadona.es',
    classifiers = [
        'Environment :: Web Environment',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
