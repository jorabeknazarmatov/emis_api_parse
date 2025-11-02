# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import Optional
from core.logger import logger
from app.client.playwright_session import PlaywrightSession, Files
from app.client.client_api import ApiClient


# ============================ ВЫСОКОУРОВНЕВЫЕ СЦЕНАРИИ ============================

class EmisExporter:
    """Фасад: авторизация, вызовы API и сохранение результатов."""
    def __init__(self, base: str) -> None:
        self.base = base
        self.session = PlaywrightSession(base, "/api/v2/auth/me/pemis/")
        self.api = ApiClient(base)

    def export_groups(self, out_name: str = "groups") -> None:
        with self.session as s:
            ctx = s.get_context()
            self.api.bind(ctx)

            me = self.api.me()
            logger.info(f"Авторизован как: {me.get('full_name')}")

            groups = self.api.fetch_groups(limit=100)
            logger.info(f"Групп получено: {len(groups)}")

            Files.save_json({"count": len(groups), "results": groups}, out_name)
            
            logger.info(f"Сохранено: {out_name}.json")

    def export_group_students(self, group_id: int, out_prefix: Optional[str] = None) -> None:
        with self.session as s:
            ctx = s.get_context()
            self.api.bind(ctx)

            me = self.api.me()
            logger.info(f"Авторизован как: {me.get('full_name')}")

            students = self.api.fetch_group_students(group_id, limit=100)
            logger.info(f"Студентов в группе {group_id}: {len(students)}")

            name = out_prefix or f"g_students_{group_id}"
            Files.save_json({"count": len(students), "results": students}, name)
            # при желании можно дополнить заголовки CSV по фактическим полям
            
            logger.info(f"Сохранено: {name}.json")
            return students

  