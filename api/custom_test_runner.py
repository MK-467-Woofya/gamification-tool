from django.test.runner import DiscoverRunner
from unittest.runner import TextTestResult, TextTestRunner

# this is inherit from unittest.runner.TextTestResult, it overwritten printErrors function
class CustomTestResult(TextTestResult):
    def printErrors(self):
        super().printErrors()
        if self.wasSuccessful():
            self.stream.writeln("All tests passed!")
        else:
            self.stream.writeln("Some tests failed.")

# this inherit from django.test.runner.DiscoverRunner, it will run Custom Test Runner
class CustomTestRunner(DiscoverRunner):
    def run_suite(self, suite, **kwargs):
        return TextTestRunner(
            verbosity=self.verbosity,
            failfast=self.failfast,
            resultclass=CustomTestResult,
        ).run(suite)