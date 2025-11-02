from __future__ import annotations
import time
from typing import Optional, Dict, Any, List
from playwright.sync_api import Page, BrowserContext, APIResponse
from core.logger import logger
from app.auth.auth import AuthHeadersProvider
from app.client.playwright_session import URLBuilder


# ============================ КЛИЕНТ API ============================

class ApiClient:
    def __init__(self, base: str) -> None:
        self.base = base
        self.me_url = URLBuilder.join(base, "/api/v2/auth/me/pemis/")
        self.groups_url = URLBuilder.join(base, "/api/v2/admin/long/group/")
        self.students_groups_url = URLBuilder.join(base, "/api/v2/admin/student/group/")
        self.headers: Optional[Dict[str, str]] = None
        self.page: Optional[Page] = None
        self.context: Optional[BrowserContext] = None
        self.auth = AuthHeadersProvider(base)

    # --- инициализация ---

    def bind(self, context: BrowserContext) -> None:
        self.context = context
        self.page = context.new_page()
        self.page.goto(self.base, wait_until="networkidle")

        # гарантированно получаем заголовки
        self.headers = self.auth.get_headers(self.page)

    # --- общие низкоуровневые операции ---

    @staticmethod
    def _should_retry(status: int) -> bool:
        return status in (401, 403, 419, 429, 498, 502, 503, 504)

    def _safe_get_with_retry(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        warm_me: bool = True,
        retries: int = 3,
        backoff: float = 0.8
    ) -> APIResponse:
        assert self.context is not None and self.page is not None
        assert self.headers is not None

        attempt = 0
        headers = dict(self.headers)

        while True:
            resp = self.context.request.get(url, params=params, headers=headers)
            if resp.ok:
                # зафиксируем последние рабочие заголовки
                self.headers = headers
                return resp

            status = resp.status
            body_preview = resp.text()[:500]
            logger.warning(f"GET {url} -> {status}; params={params} body≈{body_preview!r}")

            if attempt >= retries or not self._should_retry(status):
                return resp

            attempt += 1

            # 401/403: перечитать токен и, при необходимости, «прогреть» /me
            if status in (401, 403):
                headers = self.auth.get_headers(self.page, force_refresh=True)
                if warm_me:
                    _ = self.context.request.get(self.me_url, headers=headers)

            # 429/5xx — лёгкий бэкофф
            time.sleep(backoff * attempt)

    def _paginate(
        self,
        url: str,
        base_params: Optional[Dict[str, Any]] = None,
        limit: int = 100,
        item_key: str = "results"
    ) -> List[Dict[str, Any]]:
        """
        Универсальная пагинация:
        - Поддерживает ответы-объекты: {"count": N, "results": [...]}
        - Поддерживает ответы-списки: [ ... ]
        - Если сервер отдаёт X-Total-Count, используем его для расчёта total
        """
        results: List[Dict[str, Any]] = []
        offset, total = 0, None

        while True:
            params = dict(base_params or {})
            params.update({"limit": str(limit), "offset": str(offset)})

            resp = self._safe_get_with_retry(url, params=params, warm_me=True)
            if not resp.ok:
                raise RuntimeError(f"Ошибка {resp.status} на {url}: {resp.text()[:500]}")

            # Попробуем получить total из заголовка (если сервер даёт)
            try:
                headers = resp.headers()
                xtotal = headers.get("x-total-count") or headers.get("X-Total-Count")
                if xtotal is not None:
                    total = int(xtotal)
            except Exception:
                pass

            data = resp.json()

            # Вариант А: объект с count/results
            if isinstance(data, dict) and item_key in data:
                if total is None:
                    # берём total из тела, если не пришёл из заголовка
                    total = int(data.get("count", 0))
                batch = data.get(item_key, [])
                results.extend(batch)

                if offset + limit >= (total or len(results)):
                    break
                offset += limit
                continue

            # Вариант Б: сервер возвращает сразу список
            if isinstance(data, list):
                batch = data
                results.extend(batch)

                # Если total неизвестен, ориентируемся на размер пачки:
                # как только вернулась неполная страница — пагинация закончилась
                if total is None:
                    if len(batch) < limit:
                        break
                else:
                    if offset + limit >= total:
                        break

                offset += limit
                continue

            # Неизвестный формат — дадим понятную ошибку
            raise TypeError(
                f"Неожиданный формат ответа на {url}: {type(data).__name__}; "
                f"ожидался dict с ключом '{item_key}' или list. Превью: {str(data)[:300]}"
            )

        return results


    # --- публичные методы домена ---

    def me(self) -> Dict[str, Any]:
        resp = self._safe_get_with_retry(self.me_url, warm_me=False)
        if not resp.ok:
            raise RuntimeError(f"/auth/me/pemis/ -> {resp.status}: {resp.text()[:500]}")
        return resp.json()

    def fetch_groups(self, limit: int = 100) -> List[Dict[str, Any]]:
        return self._paginate(self.groups_url, limit=limit)

    def fetch_group_students(self, group_id: int, limit: int = 100) -> List[Dict[str, Any]]:
        return self._paginate(
            self.students_groups_url,
            base_params={"group_id": str(group_id)},
            limit=limit
        )