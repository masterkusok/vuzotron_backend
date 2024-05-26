import os
from xml.etree.ElementTree import *

from universities.models import *
from specialities.models import *

START_EVENT = 'start'
END_EVENT = 'end'


def parse_file(path: str) -> (bool, list[(University, list[Speciality])]):
    """
    This function is used to parse the xml file of Obrdnadzor registry
    Parameters
    ----------
    path : str
        path to registry.xml file
    Returns
    -------
    (bool, list[(University, list[Speciality])])
        Tuple, with bool, which indicates if registry was parsed successfully, and list on pairs of University and its specialities
    """
    university_list = []
    if not os.path.exists(path):
        # файл не найден
        return False, university_list

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
        if elem.tag == 'license' and event == START_EVENT:
            if not skip:
                print(f'University found, current number of universities is {len(university_list)}')
                if len(university_list) == 500:
                    print("500")
                university = University(short_name=short_name, full_name=full_name, city=address, region='no_data',
                                        sys_guid=sys_guid)
                university_list.append((university, current_specs))

            skip = False
            spec_skip = False
            in_license = True

        if skip:
            continue

        if elem.tag == 'schoolTypeName' and event == START_EVENT:
            if elem.text is None or elem.text != 'Образовательная организация высшего образования':
                skip = True

        if in_license and elem.tag == 'lawAddress' and event == START_EVENT:
            if elem.text is None or len(elem.text) == 0:
                skip = True
            address = elem.text

        if in_license and elem.tag == 'schoolName' and event == START_EVENT:
            if elem.text is None or len(elem.text) >= 254 or len(elem.text) == 0:
                skip = True
            full_name = elem.text

        if in_license and elem.tag == 'shortName' and event == START_EVENT:
            if elem.text is None or len(elem.text) == 0:
                skip = True
            short_name = elem.text

        if in_license and elem.tag == 'sysGuid' and event == START_EVENT:
            if elem.text is None or len(elem.text) == 0:
                skip = True
            sys_guid = elem.text

        if elem.tag == 'supplements' and event == START_EVENT:
            current_specs = []

        if elem.tag == 'licensedProgram' and event == START_EVENT:
            spec_skip = False
            spec_name = ""
            spec_code = ""
            level = ""

        if elem.tag == 'licensedProgram' and event == END_EVENT:
            spec = Speciality(name=spec_name, code=spec_code, level=level, form="no_data")
            current_specs.append(spec)

        if spec_skip:
            continue

        if elem.tag == 'code' and event == START_EVENT:
            if elem.text is None or len(elem.text) == 0:
                spec_skip = True
            spec_code = elem.text

        if elem.tag == 'name' and event == START_EVENT:
            if elem.text is None or len(elem.text) == 0:
                spec_skip = True
            spec_name = elem.text

        if elem.tag == 'eduLevelName' and event == START_EVENT:
            if elem.text is None or len(elem.text) == 0:
                spec_skip = True
            level = elem.text

    # comment
    return True, university_list
