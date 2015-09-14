from django.test import TestCase

from yaat.forms import YaatValidatorForm

from .utils import generate_columns

class TestYaatValidationForm(TestCase):
    def test_limit_offset_validation_error(self):
        columns = generate_columns()

        post = {'limit': 'sdfsdfsdf', 'offset': 'ldfksdflkm'}
        form = YaatValidatorForm(post, columns=columns)

        self.assertEqual(form.is_valid(), True)
        self.assertEqual(form.cleaned_data['limit'], form.fields['limit'].initial)
        self.assertEqual(form.cleaned_data['offset'], form.fields['offset'].initial)

    def test_no_headers_posted(self):
        columns = generate_columns()

        post = {'limit': 1, 'offset': 1}
        form = YaatValidatorForm(post, columns=columns)

        self.assertEqual(form.is_valid(), True)
        self.assertEqual(form.cleaned_data['headers'], columns)

    def test_wrong_headers_posted(self):
        columns = generate_columns()

        post = {'headers': 'sldfmksldfkmsdflk'}
        form = YaatValidatorForm(post, columns=columns)

        self.assertEqual(form.is_valid(), True)
        self.assertEqual(form.cleaned_data['headers'], columns)
        self.assertEqual(form.cleaned_data['limit'], form.fields['limit'].initial)
        self.assertEqual(form.cleaned_data['offset'], form.fields['offset'].initial)