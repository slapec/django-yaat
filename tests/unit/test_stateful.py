from copy import deepcopy

from django.contrib.auth.models import User
from django.test import TestCase

from ..utils import generate_columns
from yaat.forms import YaatValidatorForm
from yaat.models import Column


class YaatStatefulTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user')
        self.user2 = User.objects.create(username='user2')

    def test_save_state(self):
        columns = generate_columns(user=self.user)

        post = {
            'limit': 1,
            'headers': [
                {'key': 'first', 'hidden': False, 'order': Column.ASC},
                #{'key': 'second', 'hidden': False, 'order': Column.ASC},
                #{'key': 'third', 'hidden': False, 'order': Column.ASC}
            ]
        }
        form = YaatValidatorForm(post, columns=columns)

        self.assertEqual(form.is_valid(), True)

        form.save(user=self.user)
        saved_columns = list(Column.objects.filter(resource=columns[0].resource, user=self.user))

        self.assertEqual(form.cleaned_data['headers'], saved_columns)

    def test_delete_old_before_save(self):
        columns = generate_columns(user=self.user)

        for col in columns:
            col.save()

        # Save last col to different user
        new_col = deepcopy(columns[-1])
        new_col.pk = None
        new_col.user = self.user2
        new_col.save()

        self.assertEqual(Column.objects.count(), 4)

        post = {
            'limit': 1,
            'headers': [
                {'key': 'first', 'hidden': False, 'order': Column.ASC},
                {'key': 'second', 'hidden': False, 'order': Column.DESC},
                {'key': 'third', 'hidden': True, 'order': Column.ASC}
            ]
        }
        form = YaatValidatorForm(post, columns=columns)
        self.assertEqual(form.is_valid(), True)

        form.save(user=self.user)

        self.assertNotEquals(form.columns, form.cleaned_data['headers'])
        self.assertEqual(Column.objects.filter(user=self.user).count(), 3)
        self.assertEqual(Column.objects.count(), 4)
