from __future__ import annotations
import time, json, csv, re
from pathlib import Path
from typing import Optional, Dict, Any, List
from playwright.sync_api import sync_playwright, BrowserContext
from core.logger import logger
from core.config import BASE_URL, ONE_ID_URL, TARGET_URL, STATE_PATH, LOGIN, PASSWORD


# ============================ УТИЛИТЫ ============================

class URLBuilder:
    @staticmethod
    def join(base: str, path: str) -> str:
        return f"{base.rstrip('/')}/{path.lstrip('/')}"

class Files:
    @staticmethod
    def safe_name(name: str) -> str:
        return re.sub(r'[^A-Za-z0-9_.-]+', '_', name)

    @staticmethod
    def save_json(obj: Any, name: str) -> Path:
        p = Path(f"{Files.safe_name(name)}.json")
        p.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
        return p

    @staticmethod
    def save_csv(rows: List[Dict[str, Any]], headers: List[str], name: str) -> Path:
        p = Path(f"{Files.safe_name(name)}.csv")
        with p.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=headers, extrasaction="ignore")
            w.writeheader()
            for r in rows:
                w.writerow(r)
        return p



# ============================ СЕССИЯ PLAYWRIGHT ============================

class PlaywrightSession:
    """
    Управляет браузером/контекстом:
    - загрузка/сохранение storage_state
    - первичный логин через OneID
    - проверка авторизации
    """
    def __init__(self, base: str, me_path: str) -> None:
        self.base = base
        self.me_url = URLBuilder.join(base, me_path)
        self.browser = None
        self.context: Optional[BrowserContext] = None

    def __enter__(self) -> "PlaywrightSession":
        self._pw = sync_playwright().start()
        self.browser = self._pw.chromium.launch(headless=False)
        self.context = None
        return self

    def __exit__(self, exc_type, exc, tb):
        try:
            if self.context:
                self.context.close()
            if self.browser:
                self.browser.close()
        finally:
            self._pw.stop()

    # --- Вспомогательные процедуры логина ---

    def _login_and_save_state(self) -> None:
        """Одноразовый логин и сохранение storage_state.json."""
        assert self.browser is not None
        context = self.browser.new_context()
        page = context.new_page()

        page.goto(ONE_ID_URL, wait_until="networkidle")
        page.wait_for_selector('input[name="login"]', state="visible")
        page.fill('input[name="login"]', LOGIN)
        page.fill('input[name="password"]', PASSWORD)
        page.get_by_role("button", name="Кириш").click()
        logger.info("OneID: логин/пароль введены, нажата кнопка «Кириш».")

        page.wait_for_load_state("networkidle")
        page.goto(TARGET_URL, wait_until="networkidle")
        page.wait_for_load_state("networkidle")
        time.sleep(5)

        STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
        context.storage_state(path=str(STATE_PATH))
        logger.info("Cookies/localStorage сохранены в storage_state.json")
        page.close()
        context.close()

    def get_context(self) -> BrowserContext:
        """
        Возвращает авторизованный контекст.
        Если storage_state устарел — перезалогинится.
        """
        assert self.browser is not None

        if STATE_PATH.exists():
            logger.info("Пробуем войти с сохранённым storage_state...")
            ctx = self.browser.new_context(storage_state=str(STATE_PATH))

            # лёгкая экономия трафика на парсе
            ctx.route("**/*", lambda route: (
                route.abort() if route.request.resource_type in {"image", "font", "media"} else route.continue_()
            ))

            page = ctx.new_page()
            page.goto(BASE_URL, wait_until="networkidle")
            if page.url.startswith("https://oneid.edu.uz/oneid/login"):
                time.sleep(5)
            
            logger.info(f"page_url: {page.url}")
            logger.info(f"base_url: {BASE_URL}")
            if page.url != BASE_URL:
                logger.info("storage_state устарел. Запускаем повторный логин через OneID.")
                ctx.close()
                self._login_and_save_state()
                ctx = self.browser.new_context(storage_state=str(STATE_PATH))
                ctx.route("**/*", lambda route: (
                    route.abort() if route.request.resource_type in {"image", "font", "media"} else route.continue_()
                ))
            else:
                logger.info("Авторизация по cookies выполнена успешно.")
            page.close()
            self.context = ctx
            return ctx

        # storage_state нет — делаем первичный логин
        logger.info("storage_state не найден. Запускаем первичный логин через OneID.")
        self._login_and_save_state()
        ctx = self.browser.new_context(storage_state=str(STATE_PATH))
        ctx.route("**/*", lambda route: (
            route.abort() if route.request.resource_type in {"image", "font", "media"} else route.continue_()
        ))
        self.context = ctx
        return ctx
