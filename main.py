from app.parser.api_parse import EmisExporter
from app.client.playwright_session import Files
from core.logger import logger
import json

# ============================ ПРИМЕР ИСПОЛЬЗОВАНИЯ ============================

if __name__ == "__main__":
    BASE = "https://prof-emis.edu.uz"
    try:
        logger.info("Starting EmisExporter with base %s", BASE)

        exporter = EmisExporter(BASE)
        # 1) Выгрузка всех групп
        # exporter.export_groups("groups")
        
        temp_groups = [
            {"id": 23699, "name": "Hamshira 205"},
            {"id": 23698, "name": "Hamshira 204"},
            {"id": 23697, "name": "Hamshira 203"},
            {"id": 23696, "name": "Hamshira 202"},
            {"id": 23695, "name": "Fel'dsher 201"}
        ]
        
        # 2) Выгрузка студентов из группы
        group_data = dict()
        
        temp_students = list()

        for group in temp_groups:
            logger.info("Processing group %s (%s)", group.get('id'), group.get('name'))

            if group['id'] == 23695:
                curriculum_file = "feldsherlik_ishi.json"
            else:
                curriculum_file = "hamshiralik_ishi.json"

            with open(curriculum_file, "r", encoding="utf-8") as file:
                curriculum = json.load(file)

            logger.debug("Loaded curriculum from %s for group %s", curriculum_file, group.get('id'))
                        
            # O'qituvchilarni saqlash
            temp_teachers = dict()
            teacher_data = exporter.export_group_teacher(group_id=group['id'], out_prefix=None)

            logger.info("Exported %d teacher(s) for group %s", len(teacher_data or []), group.get('id'))
            
            for techer in teacher_data:
                temp_teachers['id'] = techer['id']
                temp_teachers['employee_data'] = techer['employee_data']
                temp_teachers['semester_subject'] = techer['semester_subject_data']
                temp_teachers['lecture_type'] = techer['lecture_type']
                temp_teachers['part'] = techer['part']
              
            # Guruhdagi har bir o'quvchini semestrlari билан бирга саlаш
            student_data = exporter.export_group_students(group_id=group['id'], out_prefix=None)

            logger.info("Exported %d student(s) for group %s", len(student_data or []), group.get('id'))

            for index, student in enumerate(student_data, 1):
                logger.debug("Exporting semester for student %s (group %s)", student.get('id'), group.get('id'))
                semester_data = exporter.export_semester(student_id=student['id'], out_prefix=None)
                student['semester_data'] = semester_data
                
                # Guruh o'quvchilarини bo'limларга bo'lish
                if round(len(student_data) / 2) > index:
                    student['part'] = 2
                else:
                    student['part'] = 1
                
                temp_students.append(student)
                        
                
            group_data[group['id']] = {
                "group_name": group['name'],
                "curriculum": curriculum,
                "teachers": temp_teachers,
                "students": temp_students
            }

        Files.save_json(group_data, "all_students")
        logger.info("Saved all students data to 'all_students.json' (via Files.save_json)")

    except Exception as e:
        logger.exception("Unhandled exception in main: %s", e)