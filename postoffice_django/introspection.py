import ast


def is_postoffice_django_imported(file_content: str) -> bool:
    module_tree = ast.parse(file_content)

    for node in module_tree.body:
        if isinstance(node, ast.Import):
            imported_module_names = [alias.name for alias in node.names]
            if any(map(lambda name: name.split('.')[0] == 'postoffice_django', imported_module_names)):
                return True

    return False
