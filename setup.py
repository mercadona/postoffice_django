import os
import sys
from os import path

from setuptools import find_packages, setup
from setuptools.command.install import install

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

current_directory = path.abspath(path.dirname(__file__))

with open(path.join(current_directory, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()


VERSION = '0.6.0'


class VerifyVersionCommand(install):
    description = 'Verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')

        if tag != VERSION:
            info = (f'Git tag: {tag} does not match the '
                    f'version of this app: {VERSION}')
            sys.exit(info)


setup(
    name='postoffice_django',
    version=VERSION,
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    license='APACHE License',
    description='A simple Django app to comunicate with postoffice',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mercadona/postoffice_django/',
    author='Mercadona',
    author_email='sofware.online@mercadona.es',
    classifiers=[
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
    cmdclass={
        'verify': VerifyVersionCommand,
    }
)
