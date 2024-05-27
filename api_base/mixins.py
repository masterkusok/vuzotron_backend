from django.db import models


class RegistryObjectMixIn(models.Model):
    """ "
    Mixin for object stored in registry

    Attributes
    -----------
    updated_date : datetime
        The date the object was updated last time
    auto_update : bool
        Flags if object should be automatically updated from registry.
    """

    updated_date = models.DateTimeField(auto_now=True)
    auto_update = models.BooleanField(default=True)

    class Meta:
        abstract = True
