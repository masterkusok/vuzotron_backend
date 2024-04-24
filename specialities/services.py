import models


def get_speciality(spec_id: int):
    speciality = models.Speciality.objects.get(id=spec_id)
    return speciality


def add_speciality(spec_id: int, name: str, code: str, level: str, form: str):
    if name is not None and code is not None and level is not None and form is not None:
        speciality = models.Speciality.objects.create(name=name, code=code, level=level, form=form)
        speciality.save()
        spec_id = speciality.id
    return spec_id


def delite_speciality(spec_id: int):
    speciality = models.Speciality.objects.get(id=spec_id)
    speciality.delete()
    return speciality is None


def update_speciality(spec_id: int, name: str = None, code: str = None, level: str = None, form: str = None):
    speciality = models.Speciality.objects.get(id=spec_id)
    if name is not None:
        speciality.name = models.Speciality.objects.update(name=name)
        speciality.save()
    if code is not None:
        speciality.code = models.Speciality.objects.update(code=code)
        speciality.save()
    if level is not None:
        speciality.level = models.Speciality.objects.update(level=level)
        speciality.save()
    if form is not None:
        speciality.form = models.Speciality.objects.update(form=form)
        speciality.save()
