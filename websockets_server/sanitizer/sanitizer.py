import builtins


def not_allowed(*args, **kwargs):
    print('Method is not allowed.')


builtins.open  = not_allowed
builtins.exec  = not_allowed
builtins.eval  = not_allowed
builtins.input = not_allowed

new_import = builtins.__import__


def safe_import(module_name, *args, **kwargs):
    restricted_modules = ['os', 'subprocess', 'sys']
    if module_name in restricted_modules:
        print(f'{module_name} is not allowed here.')
    else:
        return new_import(module_name, *args, **kwargs)


builtins.__import__ = safe_import
