from django.db import models


class RegistryObjectMixIn(models.Model):
    updated_date = models.DateTimeField(auto_now=True)
    auto_update = models.BooleanField(default=True)

    class Meta:
        abstract = True
