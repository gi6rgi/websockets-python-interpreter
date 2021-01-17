import builtins


new_import = builtins.__import__


def safe_import(module_name, *args, **kwargs):
    restricted_modules = ['os', 'subprocess', 'sys']
    if module_name in restricted_modules:
        print(f'{module_name} is not allowed here.')
    else:
        return new_import(module_name, *args, **kwargs)


builtins.__import__ = safe_import
