import ast

from .apps import PostofficeDjangoConfig


def is_postoffice_django_imported(file_content: str) -> bool:
    module_tree = ast.parse(file_content)

    for node in module_tree.body:
        if isinstance(node, ast.Import):
            imported_module_names = [alias.name for alias in node.names]
            if any(map(_is_postoffice_django_at_root_level, imported_module_names)):
                return True

        if isinstance(node, ast.ImportFrom) and _is_postoffice_django_at_root_level(node.module):
            return True

    return False

def _is_postoffice_django_at_root_level(imported_module_name: str) -> bool:
    root_level_module = imported_module_name.split('.')[0]

    return root_level_module == PostofficeDjangoConfig.name
