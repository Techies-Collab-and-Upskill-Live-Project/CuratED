import unittest
import sys
from django.test.runner import DiscoverRunner
from django.test import TestCase
from django.conf import settings
import os

class TestSummaryRunner(DiscoverRunner):
    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        """Run the test suite with custom output"""
        self.setup_test_environment()
        suite = self.build_suite(test_labels, extra_tests)
        print(f"\nFound {suite.countTestCases()} tests")
        
        # Print test names and modules
        print("\nTest breakdown:")
        for test in unittest.defaultTestLoader.getTestCaseNames(TestCase):
            print(f"  - {test}")
        
        # Print URL patterns
        print("\nURL patterns available:")
        from django.urls import get_resolver
        resolver = get_resolver()
        for pattern in resolver.pattern.url_patterns:
            if hasattr(pattern, 'name') and pattern.name:
                print(f"  - {pattern.name}")
        
        # Run the tests normally
        result = self.run_suite(suite)
        self.teardown_test_environment()
        return self.suite_result(suite, result)

if __name__ == "__main__":
    # Set Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    # Run the custom test runner
    runner = TestSummaryRunner()
    failures = runner.run_tests(['tests'])
    sys.exit(bool(failures))
