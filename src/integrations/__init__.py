import importlib
import pkgutil

from fastapi import FastAPI


def initialize_integrations(app: FastAPI, **kwargs):
    # Get a list of all sub-packages within the 'integrations' package
    package_path = __path__[0]
    for _, package_name, _ in pkgutil.iter_modules([package_path]):
        # Dynamically import the '__init__.py' of each sub-package
        package_module = importlib.import_module(f'{__name__}.{package_name}')

        # Check if the package has an 'initialize' function and call it
        if hasattr(package_module, 'initialize'):
            package_module.initialize(app, **kwargs)
