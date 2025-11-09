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
            logger.info("Processing group %s (%s)", group['id'], group['name'])
            
            temp_students = []
            temp_teachers = []

            curriculum_file = (
                "feldsherlik_ishi.json" if group['id'] == 23695 else "hamshiralik_ishi.json"
            )
            with open(curriculum_file, "r", encoding="utf-8") as f:
                curriculum = json.load(f)

            teacher_data = exporter.export_group_teacher(group_id=group['id'], out_prefix=None) or []
            for t in teacher_data:
                temp_teachers.append({
                    "id": t['id'],
                    "employee_data": t['employee_data'],
                    "semester_subject": t['semester_subject_data'],
                    "lecture_type": t['lecture_type'],
                    "part": t['part']
                })

            student_data = exporter.export_group_students(group_id=group['id'], out_prefix=None) or []
            half = len(student_data) // 2
            for i, s in enumerate(student_data, 1):
                s['semester_data'] = exporter.export_semester(student_id=s['id'], out_prefix=None)
                s['part'] = 1 if i <= half else 2
                temp_students.append(s)

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