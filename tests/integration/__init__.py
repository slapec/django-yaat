# coding: utf-8

import json
from unittest.mock import MagicMock

from django.test import TestCase, RequestFactory


class RestifyTestCase(TestCase):
    RESOURCE = None

    def post(self, data, raw_response=False):
        factory = RequestFactory()
        request = factory.post('/', data={}, content_type='application/json')
        request.user = MagicMock()
        request.session = {}
        request.POST = data

        resource = self.RESOURCE()
        resource.request = request
        resp = resource(request)

        if raw_response:
            return request, resp
        else:
            if resp['Content-Type'] == 'application/json':
                resp = json.loads(resp.content.decode('utf8'))
            else:
                raise ValueError('Unhandled Content-Type {0!r}'.format(resp['Content-Type']))
            return request, resp
