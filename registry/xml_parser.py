import os
from xml.etree.ElementTree import *

from universities.models import *
from specialities.models import *

START_EVENT = 'start'
END_EVENT = 'end'


def parse_file(path: str) -> (bool, list[University]):
    university_list = []
    if not os.path.exists(path):
        # файл не найден
        return False, university_list

    for event, elem in iterparse(path, events=(START_EVENT, END_EVENT)):
        # Читаем новый сертификат
        if elem.tag == 'Certificate' and event == START_EVENT:
            status_elem = elem.find('StatusName')
            if status_elem is None or status_elem.text is None or 'действ' not in status_elem.text.lower():
                # Недействующая лицензия - пропускаем
                continue

            region = elem.find('RegionName')
            full_name = elem.find('EduOrgFullName')
            short_name = elem.find('EduOrgShortName')
            sys_guid = elem.find('Id')
            if region is None or full_name is None or short_name is None or sys_guid is None:
                continue
            if region.text is None or full_name.text is None or short_name.text is None or sys_guid.text is None:
                continue
            if len(region.text) == 0 or len(full_name.text) == 0 or len(short_name.text) == 0 or len(
                    sys_guid.text) == 0:
                continue

            if University.objects.filter(system_guid=sys_guid).exists():
                university = University.objects.get(system_guid=sys_guid)
                if not university.auto_update:
                    continue
            else:
                university = University.objects.create(short_name=short_name.text, region=region.text,
                                                       city='какой то город', full_name=full_name.text,
                                                       system_guid=sys_guid.text)

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

                    if level_name.text is None or 'высш' not in level_name.text:
                        continue

                    speciality = Speciality.objects.create(name=name.text, code=code.text, level=level_name.text,
                                                           form='no_data')
                    university.specialities.add(speciality)

            if university.specialities.count() != 0:
                university_list.append(university)

    return True, university_list
