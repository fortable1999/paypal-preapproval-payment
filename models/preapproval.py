"""
payment admin page generated by template

template author: Meng Zhao fortable1999@gmail.com
"""


from django.db import models
from django.core.urlresolvers import reverse_lazy as reverse
from django.utils.translation import ugettext as _

from django_extensions.db.fields import UUIDField

from payment.models.choices import CURRENCY_CODE_CHOICES, ACTION_TYPE_CHOICES

class PreapprovalManager(models.Manager):
    """docstring for PreapprovalManager"""

    def create_preapproval(self, **kwargs):
        """docstring for create_preapproval"""
        pass


class Preapproval(models.Model):
    """
    Preapproval model
    """

    objects = PreapprovalManager()
        
    # preapprovalKey as primary key
    preapproval_id = models.CharField(
        _("pre-approval key"),
        max_length=40,
        primary_key=True,
    )

    # TODO: User GMT time
    starting_datetime = models.DateTimeField()
    ending_datetime = models.DateTimeField()

    max_amount_per_pay = models.FloatField()
    max_number_pay = models.IntegerField()
    memo = models.TextField()

    return_url = models.URLField()
    cancel_url = models.URLField()

    receiver_primary = models.ForeignKey('auth.User')
    receiver_primary_amount = models.FloatField()
    currency_code = models.CharField(
        _("Currency"),
        max_length=3, 
        choices=CURRENCY_CODE_CHOICES
    )
