# coding: utf-8

from django.test import TestCase

from yaat.resource import YaatModelResource
from yaat.forms import YaatValidatorForm
from .utils import generate_columns, generate_request, StatefulResource


class TestYaatValidationForm(TestCase):
    def test_limit_offset_validation_error(self):
        request = generate_request()
        columns = generate_columns()
        resource = YaatModelResource()

        post = {'limit': 'sdfsdfsdf', 'offset': 'ldfksdflkm'}
        form = YaatValidatorForm(post, request=request, columns=columns, resource=resource)

        self.assertEqual(form.is_valid(), True)
        self.assertEqual(form.cleaned_data['limit'], form.fields['limit'].initial)
        self.assertEqual(form.cleaned_data['offset'], form.fields['offset'].initial)

    def test_no_headers_posted(self):
        request = generate_request()
        columns = generate_columns()
        resource = YaatModelResource()

        post = {'limit': 1, 'offset': 1}
        form = YaatValidatorForm(post, request=request, columns=columns, resource=resource)

        self.assertEqual(form.is_valid(), True)
        self.assertEqual(form.cleaned_data['headers'], columns)

    def test_wrong_headers_posted(self):
        request = generate_request()
        columns = generate_columns()
        resource = YaatModelResource()

        post = {'headers': 'sldfmksldfkmsdflk'}
        form = YaatValidatorForm(post, request=request, columns=columns, resource=resource)

        self.assertEqual(form.is_valid(), True)
        self.assertEqual(form.cleaned_data['headers'], columns)
        self.assertEqual(form.cleaned_data['limit'], form.fields['limit'].initial)
        self.assertEqual(form.cleaned_data['offset'], form.fields['offset'].initial)

    def test_limit_from_resource(self):
        LIMIT = 11
        CHOICES = [1, 11, 123]

        request = generate_request()
        columns = generate_columns()

        class Resource(YaatModelResource):
            class Meta:
                resource_name = 'test'
                limit = LIMIT
                limit_choices = CHOICES
        resource = Resource()

        post = {}
        form = YaatValidatorForm(post, request=request, columns=columns, resource=resource)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.fields['limit'].initial, LIMIT)
        self.assertEqual(form.fields['limit'].choices, [(_, _) for _ in CHOICES])

    def test_stateful_init(self):
        request = generate_request()
        columns = generate_columns()
        resource = StatefulResource()

        post = {}
        form = YaatValidatorForm(post, request=request, columns=columns, resource=resource)
        self.assertTrue(form.is_valid())
        self.assertEqual(
            request.session[form.session_key(resource)],
            {'limit': form.fields['limit'].initial, 'offset': form.fields['offset'].initial}
        )

        post = {'limit': form.fields['limit'].initial, 'offset': form.fields['offset'].initial + 1, 'headers': []}  # Without "headers" the state resets itself
        form = YaatValidatorForm(post, request=request, columns=columns, resource=resource)
        self.assertTrue(form.is_valid())
        self.assertEqual(
            request.session[form.session_key(resource)],
            {'limit': form.fields['limit'].initial, 'offset': form.fields['offset'].initial + 1}
        )

    def test_invalidate_state(self):
        request = generate_request()
        columns = generate_columns()
        resource = StatefulResource()

        post = {}
        form = YaatValidatorForm(post, request=request, columns=columns, resource=resource)
        self.assertTrue(form.is_valid())
        self.assertIn(form.session_key(resource), request.session)

        form.invalidate_state()
        self.assertNotIn(form.session_key(resource), request.session)

    def test_session_key(self):
        resource = StatefulResource()
        self.assertEqual(YaatValidatorForm.session_key(resource), 'yaat_init_state_' + StatefulResource.Meta.resource_name)

    def test_limit_dict_for_resource(self):
        request = generate_request()
        resource = YaatModelResource()

        limit_dict = YaatValidatorForm.limit_dict(request, resource)
        self.assertEqual(limit_dict, {
            'limit': YaatModelResource._meta.limit,
            'options': YaatModelResource._meta.limit_choices
        })

    def test_limit_dict_for_stateful_resource(self):
        request = generate_request()
        columns = generate_columns()

        class Resource(YaatModelResource):
            class Meta:
                resource_name = 'test'
                stateful_init = True
                limit = 10
                limit_choices = [10, 20, 30]
        resource = Resource()

        post = {}
        form = YaatValidatorForm(post, request=request, columns=columns, resource=resource)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.limit_dict(request, resource), {
            'limit': Resource.Meta.limit,
            'options': Resource.Meta.limit_choices
        })

        form.invalidate_state()  # Normally the resource of the form calls this method

        post = {'limit': 20}
        form = YaatValidatorForm(post, request=request, columns=columns, resource=resource)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.limit_dict(request, resource), {
            'limit': post['limit'],
            'options': Resource.Meta.limit_choices
        })

    def test_limit_dict_for_stateful_resource_wo_state(self):
        # When a user loads the resource for the very first time his state
        # is still undefined but the limit_dict must contain something

        request = generate_request()

        class Resource(YaatModelResource):
            class Meta:
                resource_name = 'test'
                stateful_init = True
                limit = 10
                limit_choices = [10, 20, 30]
        resource = Resource()

        self.assertEqual(YaatValidatorForm.limit_dict(request, resource), {
            'limit': Resource.Meta.limit,
            'options': Resource.Meta.limit_choices
        })