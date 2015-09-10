# coding: utf-8

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from ordered_model.models import OrderedModel


class Column(OrderedModel):
    ORDER_DISALLOWED = None
    UNORDERED = 0
    ASC = 1
    DESC = 2

    HIDE_DISALLOWED = None

    ORDER_CHOICES = (
        (ORDER_DISALLOWED, _('Ordering disallowed')),
        (UNORDERED, _('Unordered')),
        (ASC, _('Ascending')),
        (DESC, _('Descending'))
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('User'), related_name='column_users')

    resource = models.CharField(max_length=64, verbose_name=_('Resource name'))
    key = models.CharField(max_length=64, verbose_name=_('Column key'))
    is_shown = models.NullBooleanField(default=True, verbose_name=_('Show field'))
    ordering = models.PositiveSmallIntegerField(choices=ORDER_CHOICES, default=UNORDERED, null=True,
                                                verbose_name=_('Field order'))

    order_with_respect_to = ('resource', 'user')

    class Meta:
        unique_together = ('resource', 'user', 'key')

    def __init__(self, key, value, *args, is_virtual=True, **kwargs):
        self.value = value
        self.is_virtual = is_virtual
        super().__init__(*args, key=key, **kwargs)

        if self.is_virtual:
            self.ordering = self.ORDER_DISALLOWED

    def __eq__(self, other):
        left = [self.user_id, self.resource, self.key, self.order, self.is_shown, self.ordering]
        right = [other.user_id, other.resource, other.key, other.order, other.is_shown, other.ordering]

        return left == right

    def get_ordering(self):
        if self.ordering == self.ASC:
            return self.key
        elif self.ordering == self.DESC:
            return '-' + self.key

    def flatten(self):
        data = {
            'key': self.key,
            'value': str(self.value)
        }

        if self.ordering != self.ORDER_DISALLOWED:
            data['order'] = self.ordering

        if self.is_shown is not None:
            data['hidden'] = not self.is_shown

        return data
