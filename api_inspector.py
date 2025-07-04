import os
import importlib
import inspect
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

# Import relevant modules
from django.urls import get_resolver
from django.urls.resolvers import URLPattern, URLResolver

def print_all_urls():
    """Print all URL patterns defined in the project"""
    print("\n=== URL PATTERNS ===")
    resolver = get_resolver()
    
    def _get_patterns(resolver, prefix=''):
        patterns = []
        for pattern in resolver.url_patterns:
            if isinstance(pattern, URLPattern):
                patterns.append(f"{prefix}{pattern.pattern} → {pattern.name or 'unnamed'}")
            elif isinstance(pattern, URLResolver):
                patterns.extend(_get_patterns(pattern, prefix=f"{prefix}{pattern.pattern}"))
        return patterns
    
    for pattern in sorted(_get_patterns(resolver)):
        print(pattern)

def inspect_module(module_name):
    """Print all functions in a module"""
    print(f"\n=== FUNCTIONS IN {module_name} ===")
    try:
        module = importlib.import_module(module_name)
        for name, obj in inspect.getmembers(module):
            if inspect.isfunction(obj):
                print(f"- {name}")
    except (ImportError, ModuleNotFoundError):
        print(f"Module {module_name} not found")

if __name__ == "__main__":
    print_all_urls()
    
    # Inspect key modules
    modules_to_inspect = [
        'api.views',
        'api.youtube',
        'api.services.youtube_service',
        'playlists.views'
    ]
    
    for module in modules_to_inspect:
        inspect_module(module)
