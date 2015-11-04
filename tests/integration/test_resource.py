# coding: utf-8

import math

from django.contrib.auth.models import User
from tests.integration import RestifyTestCase
from tests.models import Item
from yaat.forms import YaatValidatorForm

from yaat.resource import YaatModelResource


class Resource(YaatModelResource):
    class Meta:
        resource_name = 'resource'
        model = Item
        columns = ('name', 'quantity', 'price')
        stateful_init = True


class TestYaatModelResource(RestifyTestCase):
    fixtures = ['tests/fixtures']
    RESOURCE = Resource

    def setUp(self):
        self.user = User.objects.create(username='user')

    def test_fixtures_loaded(self):
        # This always tricks me
        self.assertGreater(Item.objects.count(), 0)

    def test_reset_offset_empty_page(self):
        request, first_page = self.post({})
        limit = len(first_page['rows'])
        item_count = Item.objects.count()
        self.assertGreater(limit, 0)
        pages = math.ceil(item_count / limit)

        for offset in range(pages+10):  # Over-iterate pages
            request, data = self.post({'offset': offset+1})  # Page index is not zero-based
            if offset >= 2:  # 3rd page does not exists. Resource must always return with the 1st page
                self.assertEqual(data, first_page)

        self.assertEqual(
            request.session[YaatValidatorForm.session_key(self.RESOURCE)]['offset'],
            YaatValidatorForm.base_fields['offset'].initial
        )

