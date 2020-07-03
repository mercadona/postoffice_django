from postoffice_django.introspection import is_postoffice_django_imported


class TestIsPostOfficeDjangoImported:

    def test_not_imported_when_empty_file(self):
        file_content = ''

        assert not is_postoffice_django_imported(file_content)

    
    class TestFilesWithImportStatements:

        def test_imported_when_postoffice_django_is_imported(self):
            file_content = (
                'import django\n'
                'import postoffice_django\n'
                'import rest_framework\n'
            )

            assert is_postoffice_django_imported(file_content)

        def test_imported_when_postoffice_django_is_imported_with_alias(self):
            file_content = (
                'import django\n'
                'import postoffice_django as po\n'
                'import rest_framework\n'
            )

            assert is_postoffice_django_imported(file_content)

        def test_imported_when_postoffice_django_submodule_is_imported(self):
            file_content = (
                'import django\n'
                'import postoffice_django.publishing\n'
                'import rest_framework\n'
            )

            assert is_postoffice_django_imported(file_content)

        def test_imported_when_postoffice_django_submodule_is_imported_with_alias(self):
            file_content = (
                'import django\n'
                'import postoffice_django.publishing as publishing\n'
                'import rest_framework\n'
            )

            assert is_postoffice_django_imported(file_content)

        def test_not_imported_when_module_contains_other_import_statements(self):
            file_content = (
                'import collections\n'
                'import datetime\n'
                'import functools\n'
            )

            assert not is_postoffice_django_imported(file_content)

        def test_not_imported_when_module_name_contains_postoffice_django(self):
            file_content = (
                'import postoffice_django_lasjdf\n'
                'import postoffice_django_lasjdf.publishing\n'
                'import foo.postoffice_django\n'
                'import foo.postoffice_django.bar\n'
            )

            assert not is_postoffice_django_imported(file_content)


    class TestFilesWithImportFromStatements:

        def test_imported_when_postoffice_django_is_imported(self):
            file_content = (
                'import django\n'
                'from postoffice_django import publishing\n'
                'from rest_framework import generics \n'
            )

            assert is_postoffice_django_imported(file_content)

        def test_imported_when_postoffice_django_is_imported_with_alias(self):
            file_content = (
                'import django\n'
                'from postoffice_django import publishing as p\n'
                'from rest_framework import generics as g\n'
            )

            assert is_postoffice_django_imported(file_content)

        def test_imported_when_postoffice_django_submodule_is_imported(self):
            file_content = (
                'import django\n'
                'from postoffice_django.config import configure_topics\n'
                'from rest_framework.generics import GenericAPIView\n'
            )

            assert is_postoffice_django_imported(file_content)

        def test_imported_when_postoffice_django_submodule_is_imported_with_alias(self):
            file_content = (
                'import django\n'
                'from postoffice_django.config import configure_topics as ct\n'
                'from rest_framework.generics import GenericAPIView as gav\n'
            )

            assert is_postoffice_django_imported(file_content)
