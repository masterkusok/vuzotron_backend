import models


def get_speciality(target_id):
    speciality = models.Speciality.objects.get(id=target_id)
    return speciality


def add_speciality(name: str, code: str, level: str, form: str):
    speciality = models.Speciality.objects.create(name=name, code=code, level=level, form=form)
    speciality.save()
    target_id = speciality.id
    return target_id


def delete_speciality(target_id: int):
    speciality = models.Speciality.objects.get(id=target_id)
    speciality.delete()
    return speciality is None


def update_speciality(name: str, code: str, level: str, form: str):
    speciality = models.Speciality.objects.update(name=name, code=code, level=level, form=form)
    speciality.save()
