# coding: utf-8

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Column(models.Model):
    ORDER_DISALLOWED = None
    UNORDERED = 0
    ASC = 1
    DESC = 2

    ORDER_CHOICES = (
        (ORDER_DISALLOWED, _('Ordering disallowed')),
        (UNORDERED, _('Unordered')),
        (ASC, _('Ascending')),
        (DESC, _('Descending'))
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('User'))

    resource = models.CharField(max_length=64, verbose_name=_('Resource name'))
    order = models.PositiveIntegerField(verbose_name=_('Column order'))
    key = models.CharField(max_length=64, verbose_name=_('Column key'))
    is_shown = models.NullBooleanField(default=True, verbose_name=_('Show field'))
    ordering = models.PositiveSmallIntegerField(choices=ORDER_CHOICES, default=UNORDERED, null=True,
                                                verbose_name=_('Field order'))

    def as_dict(self):
        return {
            'user': self.user,
            'resource': self.resource,
            'order': self.order,
            'key': self.key,
            'is_shown': self.is_shown,
            'ordering': self.ordering,
        }
