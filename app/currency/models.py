from django.db import models
from django.utils.translation import gettext_lazy as _


class Currency(models.Model):
    name = models.CharField(_('name'), max_length=30, unique=True)

    def __str__(self):
        return self.name


class Rate(models.Model):
    currency = models.ForeignKey(Currency, _('currency'), related_name='rates')
    date = models.DateField(_('date'))
    rate = models.FloatField(_('Last execution during the time frame'))  # CLOSE
    volume = models.FloatField(_('Quantity of symbol traded within the timeframe'))  # VOLUME
    mts = models.BigIntegerField(_('millisecond time stamp'), default=0)

    def __str__(self):
        return '{} - {}'.format(self.currency, self.date)

    class Meta:
        ordering = ['-mts']
        verbose_name = _("Rate")
        verbose_name_plural = _("Rates")
        unique_together = ['currency', 'mts']
