import builtins


builtins.open  = lambda *args, *kwargs: print('Built-in function "open" is not allowed.')
builtins.exec  = lambda *args, *kwargs: print('Built-in function "exec" is not allowed.')
builtins.eval  = lambda *args, *kwargs: print('Built-in function "exal" is not allowed.')
builtins.input = lambda *args, *kwargs: print('Built-in function "input" is not allowed.')

new_import = builtins.__import__


def safe_import(module_name, *args, **kwargs):
    restricted_modules = ['os', 'subprocess', 'sys']
    if module_name in restricted_modules:
        print(f'{module_name} is not allowed here.')
    else:
        return new_import(module_name, *args, **kwargs)


builtins.__import__ = safe_import
