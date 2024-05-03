from .models import *


def get_one(target_id) -> Speciality:
    """
    This method is used go get speciality from database
    Parameters
    ---------
    target_id : int
        Id of target speciality
    Returns
    ---------
    Speciality
        Speciality object, if speciality with such was found in database, otherwise None
    """
    if Speciality.objects.filter(id=target_id).exists():
        speciality = Speciality.objects.get(id=target_id)
        return speciality
    return None


def get_list() -> list[Speciality]:
    """
    This method is used to get list of all specialities from database
    Returns
    list[Speciality]
    ---------
        Returns list of all specialities in database
    """
    return Speciality.objects.all()


def add(name: str, code: str, level: str, form: str, auto_update: bool = False) -> int:
    """
    This method is used to add new speciality to database.
    Parameters
    ----------
    name : str
        Name of speciality
    code : str
        Code of speciality
    level : str
        Educational level of speciality (bachelor, specialist etc.)
    form : str
        Form of education
    auto_update : bool
        This flag tells registry component if we should pull updates from remote registry to db.
         By default, it is set to False
    Returns
    ----------
    int
        Returns id of created speciality
    """
    speciality = Speciality.objects.create(name=name, code=code, level=level, form=form, auto_update=auto_update)
    return speciality.id


def add_list(specialities: list[Speciality]) -> list[int]:
    """
    This method is used to insert list of specialities into database.
    Parameters
    ----------
    specialities : list[Speciality]
        List of specialities to be added
    Returns
    ----------
    list[int]
        Returns list of ids of added specialities
    """
    specialities = Speciality.objects.bulk_create(specialities)
    return [spec.id for spec in specialities]


def delete(target_id: int) -> bool:
    """
    This method is used to delete speciality from database
    Parameters
    ---------
    target_id : int
        Id of target speciality
    Returns
    ---------
    bool
        Returns true if speciality was deleted, false otherwise
    """
    if Speciality.objects.filter(id=target_id).exists():
        Speciality.objects.get(id=target_id).delete()
        return True
    return False


def update(target_id: int, name: str, code: str, level: str, form: str, auto_update: bool = False) -> bool:
    """
    This method is used to update speciality fields in database.
    Parameters
    ----------
    target_id : int
        Id of speciality to be updated
    name : str
        New name of speciality
    code : str
        New code of speciality
    level : str
        New educational level of speciality (bachelor, specialist etc.)
    form : str
        New form of education
    auto_update : bool
        New value for auto_update. By default, it updates to False.
    Returns
    ----------
    bool
        Returns true if speciality was updated, false otherwise
    """
    if Speciality.objects.filter(id=target_id).exists():
        Speciality.objects.update(name=name, code=code, level=level, form=form, auto_update=auto_update)
        return True
    return False
