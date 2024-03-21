from django.test import TestCase
from _database.models import Term

class TermModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Term.objects.create(name="Sebastian")

    def test_name_label(self):
        term = Term.objects.get(id=1)
        field_label = term._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")
    
    def test_name_max_length(self):
        term = Term.objects.get(id=1)
        max_length = term._meta.get_field("name").max_length
        self.assertEqual(max_length, 100)
