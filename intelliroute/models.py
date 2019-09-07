import uuid
from django.db import models
from simple_history.models import HistoricalRecords


ACTIVE='A'
INACTIVE='I'
DELETED='D'

MODEL_STATUS_CHOICES = ((ACTIVE, 'Active'), 
                        (INACTIVE, 'In-active'), 
                        (DELETED, 'Deleted'))

HTTP_METHOD_CHOICES = (('GET', 'Get'),
                       ('POST', 'Post'),
                       ('PUT', 'Put'),
                       ('DELETE', 'Delete'),
                        ('PATCH', 'Patch'))


class BaseManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=ACTIVE)


class BaseModel(models.Model):
    """
    This model has base attributes that would be inherited by all other models
    """
    status = models.CharField(max_length=1, choices=MODEL_STATUS_CHOICES, default=ACTIVE)
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
    objects = BaseManager()
    
    class Meta:
        abstract = True

class IntegratingApp(BaseModel):
    name = models.CharField(max_length=100)
    base_url = models.CharField(max_length=100)
    alias = models.CharField(max_length=10, unique=True)
    
class RequestAudit(BaseModel):
    request_url = models.CharField(max_length=250, blank=True, null=True)
    http_method = models.CharField(max_length=6, choices=HTTP_METHOD_CHOICES)
    response_time = models.DecimalField(max_digits=10, decimal_places=8)
    response_code = models.CharField(max_length=5, blank=True, null=True)
    integrating_app = models.ForeignKey(
        IntegratingApp, related_name='integrating_app', on_delete=models.PROTECT)
    history = HistoricalRecords()

    def integrating_app__name(self):
        return u'{}'.format(self.integrating_app.name)

