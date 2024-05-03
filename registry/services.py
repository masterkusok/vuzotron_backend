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
    # response = requests.get(url, stream=True)
    # cacher = backend.settings.REDIS_CACHER
    # if response.status_code != HTTPStatus.OK:
    #     print("Invalid url")
    #     return False
    #
    # with open('registry.zip', mode='wb') as file:
    #     for chunk in response.iter_content(chunk_size=10 * 1024):
    #         print(f'downloading registry zip... downloaded {len(chunk)} bytes')
    #         file.write(chunk)
    #
    # with open("registry.zip", mode="rb") as file:
    #     registry_hash = hashlib.md5()
    #     while chunk := file.read():
    #         registry_hash.update(chunk)
    #
    # actual_hash = cacher.get('hash')
    # if actual_hash == registry_hash.digest():
    #     print('registry has not changed')
    #     return False
    #
    # cacher.set('hash', registry_hash.digest())
    # with zipfile.ZipFile('registry.zip', 'r') as zip_origin:
    #     zip_origin.extractall('temp/')
    #

    ok, parsed_universities = parse_file('temp/' + os.listdir('temp/')[0])

    if not ok:
        print('cant handle parsing ')
        return False

    for university, specialities in parsed_universities:
        if not (University.objects.filter(system_guid=university.system_guid).exists()):
            university.save()
            university.specialities.add(specialities)
            continue

        db_university = University.objects.update()



    os.remove('registry.zip')
    shutil.rmtree('temp')
    return True
