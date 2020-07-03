from postoffice_django.introspection import is_postoffice_django_imported


class TestIsPostOfficeDjangoImported:

    def test_not_imported_when_empty_file(self):
        file_content = ''

        assert not is_postoffice_django_imported(file_content)

    
    class TestFilesWithImportStatements:

        def test_imported_when_postoffice_django_appears_in_import_statement(self):
            file_content = (
                'import django\n'
                'import postoffice_django\n'
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
