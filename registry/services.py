import hashlib
from http import HTTPStatus
import requests
import zipfile
import shutil

import backend.settings
from .xml_parser import *


def pull_registry_data(url: str) -> bool:
    """
    This method is used to pull data from xml-registry to DB.
    Parameters
    ---------
    url : str
        The URL of the xml file, registry is stored in.
    Returns
    ---------
    bool
        Returns True, if data in DB was updated.
    """


    # парсим файл
    ok, university_list = parse_file('temp/' + os.listdir('temp/')[0])

    if not ok:
        print('cant handle parsing ')
        return False

    # обновим данные в БД
    for university in university_list:
        if University.objects.filter(system_guid=university.system_guid).exists():
            # Обновление данных по университету, которых уже представлен в базе
            db_university = University.objects.get(system_guid=university)
            if not db_university:
                University.objects.create(system_guid=university.system_guid, short_name=university.short_name,
                                          region=university.region, city=university.city,
                                          full_name=university.full_name)
            if db_university.auto_update:  # Если университет обновлялся руками, его не трогаем
                db_university = university
                db_university.save()

    os.remove('registry.zip')
    shutil.rmtree('temp')
    return True
