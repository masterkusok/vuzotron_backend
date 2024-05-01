from django.db import models


class Speciality(models.Model):
    name = models.CharField(max_length=255, null=True)
    code = models.CharField(max_length=63, null=True)
    level = models.CharField(max_length=63, null=True)
    form = models.CharField(max_length=63, null=True)
    updated_date = models.DateTimeField(auto_now=True)
    auto_update = models.BooleanField(default=True)

    @classmethod
    def create_speciality(cls, name: str, code: str, level: str, form: str):
        return cls(name=name, code=code, level=level, form=form)
