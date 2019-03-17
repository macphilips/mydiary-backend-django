from django.test import TestCase

# Create your tests here.
from django.test import TestCase

from modules.entries.models import Entry


class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Entry.objects.create(title='Big', content='Bob')

    def test_date_of_death_label(self):
        author = Entry.objects.get(id=1)
        field_label = author._meta.get_field('date_of_death').verbose_name
        self.assertEquals(field_label, 'died')

    def test_title_max_length(self):
        author = Entry.objects.get(id=1)
        max_length = author._meta.get_field('title').max_length
        self.assertEquals(max_length, 20)

    def test_object_name_is_last_name_comma_first_name(self):
        author = Entry.objects.get(id=1)
        expected_object_name = '{author.last_name}, {author.first_name}'
        self.assertEquals(expected_object_name, str(author))

    def test_get_absolute_url(self):
        author = Entry.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEquals(author.get_absolute_url(), '/catalog/author/1')
