import unittest
import inspect
from importlib import import_module

class FunctionDiscoveryTest(unittest.TestCase):
    """Helper tests to discover actual function names in modules"""
    
    @unittest.skip("Only run manually to discover functions")
    def test_discover_functions(self):
        """Print available functions in modules to help with mocking"""
        modules_to_inspect = [
            'api.views', 
            'api.services.youtube',
            'api.utils',
            'api.services.youtube_service'
        ]
        
        for module_name in modules_to_inspect:
            try:
                module = import_module(module_name)
                print(f"\nFunctions in {module_name}:")
                for name, obj in inspect.getmembers(module):
                    if inspect.isfunction(obj):
                        print(f"  - {name}")
            except (ImportError, ModuleNotFoundError):
                print(f"Module {module_name} not found")
