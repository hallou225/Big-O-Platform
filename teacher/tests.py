from django.test import TestCase

# Create your tests here.
class TeacherTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        pass
    
    def setUp(self):
        print("setUp: Run once for every test method to set up clean data.")
        pass

    def test_false_is_false(self):
        print("Method: test_false_is_false.")
        self.assertFalse(False)

    def test_false_is_true(self):
        print("Method: test_false_is_true.")
        self.assertTrue(False)

    def test_one_plus_one_equals_two(self):
        print("Method: test_one_plus_one_equals_two.")
        self.assertEqual(1 + 1, 2)

"""
NOTE: user$ python manage.py test
        ... will discover all files named with the pattern test*.py under the current directory and run
        all tests defined using appropriate base classes.

        By default, the tests will individually report only on test failures, followed by a test summary.

        Any error similar to "ValueError: Missing staticfiles manifest entry..." when running tests can
        can fixed by simply running "$ python manage.py collectstatic" before running the tests.

        When running "user$ python manage.py test", you can append "--verbosity" and specify a number from
        0 (least descriptive) to 3 (most descriptive) to show more/less information when running the tests.
            Example: python manage.py test --verbosity 2
        
        Running Specific Tests:
            Run a specified module: "user$ python manage.py test APPNAME.tests"
            Example: "user$ python manage.py test teacher.tests"

            Run a specified class: "user$ python manage.py test teacher.tests.CLASSNAME"
            Example: "user$ python manage.py test teacher.tests.TeacherTests"

            Run a specified test: "user$ python manage.py test teacher.tests.TeacherTests.TESTNAME"
            Example: "user$ python manage.py test teacher.tests.TeacherTests.test_one_plus_one_equals_two"
        
"""
