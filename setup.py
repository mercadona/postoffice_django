import os

from setuptools import find_packages, setup


README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name = 'postoffice_django',
    version = '0.1',
    packages=find_packages(exclude=("tests",)),
    include_package_data = True,
    license = 'APACHE License', 
    description = 'A simple Django app to comunicate with post office',
    long_description = README,
    url = 'http://www.example.com/',
    author = 'Your Name',
    author_email = 'yourname@example.com',
    classifiers = [
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License', # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
