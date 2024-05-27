import hashlib
import os
import shutil
import zipfile
from http import HTTPStatus
from xml.etree.ElementTree import iterparse

import redis
import requests

import backend.settings
from specialities.models import Speciality
from universities.models import University
from universities.services import UniversityServices

START_EVENT = "start"
END_EVENT = "end"


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
    response = requests.get(url, stream=True)
    cacher = backend.settings.REDIS_CACHER
    if response.status_code != HTTPStatus.OK:
        print("Invalid url")
        return False

    with open("registry.zip", mode="wb") as file:
        for chunk in response.iter_content(chunk_size=10 * 1024):
            print(f"downloading registry zip... downloaded {len(chunk)} bytes")
            file.write(chunk)

    with open("registry.zip", mode="rb") as file:
        registry_hash = hashlib.md5()
        while chunk := file.read():
            registry_hash.update(chunk)
    try:
        actual_hash = cacher.get("hash")
        if actual_hash == registry_hash.digest():
            print("registry has not changed")
            return False
        cacher.set("hash", registry_hash.digest())
    except redis.exceptions.ConnectionError:
        print("Cant access RedisCache")
        clear_temp_data()
        return False

    with zipfile.ZipFile("registry.zip", "r") as zip_origin:
        zip_origin.extractall("temp/")

    parse_file("temp/" + os.listdir("temp/")[0])

    clear_temp_data()
    return True


def clear_temp_data():
    """
    This method is used to clear temp folders with registry files
    """
    if os.path.exists("registry.zip"):
        os.remove("registry.zip")
    if os.path.exists("temp"):
        shutil.rmtree("temp")


def push_universities_to_db(parsed_universities: list[(University, list[Speciality])]):
    """
    This method is used to write new universities from registry to database
    Parameters
    ----------
    parsed_universities : list[tuple(University, list[Speciality])]
        list of new universities to be added

    Returns
    -------

    """
    university_services = UniversityServices()
    print("Moving universities to DB")
    for university, specialities in parsed_universities:
        db_university = university_services.get_by(sys_guid=university)
        if not db_university:
            db_university = university_services.add_one(
                short_name=university.short_name,
                full_name=university.full_name,
                region=university.region,
                city=university.city,
                auto_update=True,
                sys_guid=university.sys_guid,
            )
        else:
            result = university_services.update(
                db_university.id,
                short_name=university.short_name,
                full_name=university.full_name,
                region=university.region,
                city=university.city,
                auto_update=True,
                sys_guid=university.sys_guid,
            )
            if not result:
                continue
        db_university.save()
        for spec in specialities:
            spec.save()
        db_university.specialities.set(specialities)


def parse_file(path: str):
    """
    This function is used to parse the xml file of Obrdnadzor registry
    Parameters
    ----------
    path : str
        path to registry.xml file
    Returns
    -------
    (bool, list[(University, list[Speciality])])
        Tuple, with bool, which indicates if registry was parsed successfully
        , and list on pairs of University and its specialities
    """
    university_list = []
    if not os.path.exists(path):
        # файл не найден
        return

    in_license = True
    skip = False
    spec_skip = False
    address = ""
    short_name = ""
    full_name = ""
    sys_guid = ""
    spec_name = ""
    spec_code = ""
    level = ""

    current_specs = []

    for event, elem in iterparse(path, events=(START_EVENT, END_EVENT)):
        # Читаем новый сертификат
        if elem.tag == "license" and event == START_EVENT:
            if not skip:
                print(
                    f"University found, current number of universities is"
                    f" {len(university_list)}"
                )
                if len(university_list) >= 100:
                    push_universities_to_db(university_list)
                    university_list = []

                university = University(
                    short_name=short_name,
                    full_name=full_name,
                    city=address,
                    region="no_data",
                    sys_guid=sys_guid,
                )
                university_list.append((university, current_specs))

            skip = False
            spec_skip = False
            in_license = True

        if skip:
            elem.clear()
            continue

        if elem.tag == "schoolTypeName" and event == START_EVENT:
            if (
                    elem.text is None
                    or elem.text != "Образовательная организация высшего образования"
            ):
                skip = True

        if in_license and elem.tag == "lawAddress" and event == START_EVENT:
            if elem.text is None or len(elem.text) == 0:
                skip = True
            address = elem.text

        if in_license and elem.tag == "schoolName" and event == START_EVENT:
            if elem.text is None or len(elem.text) >= 254 or len(elem.text) == 0:
                skip = True
            full_name = elem.text

        if in_license and elem.tag == "shortName" and event == START_EVENT:
            if elem.text is None or len(elem.text) == 0:
                skip = True
            short_name = elem.text

        if in_license and elem.tag == "sysGuid" and event == START_EVENT:
            if elem.text is None or len(elem.text) == 0:
                skip = True
            sys_guid = elem.text

        if elem.tag == "supplements" and event == START_EVENT:
            current_specs = []

        if elem.tag == "licensedProgram" and event == START_EVENT:
            spec_skip = False
            spec_name = ""
            spec_code = ""
            level = ""

        if (not spec_skip) and elem.tag == "licensedProgram" and event == END_EVENT:
            spec = Speciality(
                name=spec_name, code=spec_code, level=level, form="no_data"
            )
            current_specs.append(spec)

        if spec_skip:
            elem.clear()
            continue

        if elem.tag == "code" and event == START_EVENT:
            if elem.text is None or len(elem.text) == 0:
                spec_skip = True
            spec_code = elem.text

        if elem.tag == "name" and event == START_EVENT:
            if elem.text is None or len(elem.text) == 0:
                spec_skip = True
            spec_name = elem.text

        if elem.tag == "eduLevelName" and event == START_EVENT:
            if elem.text is None or len(elem.text) == 0:
                spec_skip = True
            level = elem.text
        elem.clear()
    if len(university_list) != 0:
        push_universities_to_db(university_list)
