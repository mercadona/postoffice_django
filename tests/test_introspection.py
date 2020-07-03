from postoffice_django.introspection import is_postoffice_django_imported


class TestIsPostOfficeDjangoImported:

    def test_returns_false_when_empty_file(self):
        file_content = ''

        assert not is_postoffice_django_imported(file_content)
