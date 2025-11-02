from app.parser.api_parse import EmisExporter
from app.client.playwright_session import Files

# ============================ ПРИМЕР ИСПОЛЬЗОВАНИЯ ============================

if __name__ == "__main__":
    BASE = "https://prof-emis.edu.uz"

    exporter = EmisExporter(BASE)
    # 1) Выгрузка всех групп
    # exporter.export_groups("groups")
    temp_students = dict()
    temp_groups = [23699, 23698, 23697, 23696, 23695]
    
    # 2) Выгрузка студентов из группы
    for group_id in temp_groups:
        students = exporter.export_group_students(group_id=group_id, out_prefix=None)
        temp_students[group_id] = {"group_name": '', "students": students}
    
    Files.save_json(temp_students, "all_group_students")  