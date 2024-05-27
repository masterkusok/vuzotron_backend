import hashlib
from http import HTTPStatus
import requests
import zipfile
import shutil
from universities.services import *
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

    # # парсим файл
    response = requests.get(url, stream=True)
    cacher = backend.settings.REDIS_CACHER
    if response.status_code != HTTPStatus.OK:
        print("Invalid url")
        return False

    with open('registry.zip', mode='wb') as file:
        for chunk in response.iter_content(chunk_size=10 * 1024):
            print(f'downloading registry zip... downloaded {len(chunk)} bytes')
            file.write(chunk)

    with open("registry.zip", mode="rb") as file:
        registry_hash = hashlib.md5()
        while chunk := file.read():
            registry_hash.update(chunk)

    actual_hash = cacher.get('hash')
    if actual_hash == registry_hash.digest():
        print('registry has not changed')
        return False

    cacher.set('hash', registry_hash.digest())
    with zipfile.ZipFile('registry.zip', 'r') as zip_origin:
        zip_origin.extractall('temp/')

    ok, parsed_universities = parse_file('temp/' + os.listdir('temp/')[0])

    if not ok:
        print('cant handle parsing ')
        return False

    university_services = UniversityServices()
    print('Moving universities to DB')
    for university, specialities in parsed_universities:
        db_university = university_services.get_by(sys_guid=university)
        if not db_university:
            db_university = university_services.add_one(short_name=university.short_name,
                                                        full_name=university.full_name,
                                                        region=university.region, city=university.city,
                                                        auto_update=True,
                                                        sys_guid=university.sys_guid)
        else:
            result = university_services.update(db_university.id, short_name=university.short_name,
                                                full_name=university.full_name,
                                                region=university.region, city=university.city,
                                                auto_update=True,
                                                sys_guid=university.sys_guid)
            if not result:
                continue
        db_university.save()
        for spec in specialities:
            spec.save()
        db_university.specialities.set(specialities)

    os.remove('registry.zip')
    shutil.rmtree('temp')
    return True
