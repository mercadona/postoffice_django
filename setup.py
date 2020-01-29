import os

from setuptools import find_packages, setup


README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name = 'postoffice_django',
    version = '0.1',
    description = 'Postoffice django client',
    long_description = README,
    author = 'MercadonaTech',
    author_email = 'software.online@mercadona.es',
    url = 'http://github.com/mercadona/postoffice_django',
    packages=find_packages(exclude=("tests",)),
    include_package_data = True,
    install_requires=[
        'django',
        'requests'
    ]
    license='Apache Software License 2.0',
    keywords='postoffice'
    classifiers = [
        'Environment :: Web Environment',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
