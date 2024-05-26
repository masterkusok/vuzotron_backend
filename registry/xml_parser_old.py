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

    for event, elem in iterparse(path, events=(START_EVENT, END_EVENT)):
        # Читаем новый сертификат
        if elem.tag == 'Certificate' and event == START_EVENT:
            organization = elem.find('ActualEducationOrganization')
            if not organization:
                continue
            region = organization.find('RegionName')
            full_name = organization.find('FullName')
            short_name = organization.find('ShortName')
            sys_guid = organization.find('Id')
            if region is None or full_name is None or short_name is None or sys_guid is None:
                continue
            if region.text is None or full_name.text is None or short_name.text is None or sys_guid.text is None:
                continue
            if len(region.text) == 0 or len(full_name.text) == 0 or len(short_name.text) == 0 or len(
                    sys_guid.text) == 0:
                continue

            university = University(region=region.text, full_name=full_name.text, short_name=short_name.text,
                                    sys_guid=sys_guid.text, city='no_data')
            specs = []

            supplements = elem.find('Supplements')
            if supplements is None:
                continue
            for supplement in supplements:
                programs = supplement.find('EducationalPrograms')
                if programs is None:
                    continue
                for program in programs:
                    level_name = program.find("EduLevelName")
                    name = program.find("ProgrammName")
                    code = program.find("ProgrammCode")
                    if level_name is None or name is None or code is None:
                        continue

                    if (level_name.text is None or name.text is None or code.text is None) or (
                            level_name == '' or name.text == '' or code.text == '' or name.text == ''):
                        continue

                    if 'высш' not in level_name.text.lower():
                        continue

                    speciality = Speciality(name=name.text, code=code.text, level=level_name.text, form='no_data')
                    specs.append(speciality)

            if len(specs) != 0:
                university_list.append((university, specs))
                print(f'University found. Current number of universities is {len(university_list)}')
    # comment
    return True, university_list
