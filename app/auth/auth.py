# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import Optional, Tuple, Dict
from playwright.sync_api import sync_playwright, Page
from core.logger import logger


# ============================ АВТОРИЗАЦИЯ ============================

class AuthHeadersProvider:
    """Отвечает за ожидание появления токена в localStorage, чтение токена и сбор заголовков."""
    def __init__(self, base: str) -> None:
        self.base = base
        self._headers: Optional[Dict[str, str]] = None

    def wait_token(self, page: Page, timeout_ms: int = 7000) -> None:
        page.wait_for_function(
            """() => !!(localStorage.getItem('access') || localStorage.getItem('token') || localStorage.getItem('auth'))""",
            timeout=timeout_ms
        )

    def extract_token_and_scheme(self, page: Page) -> Tuple[str, str]:
        token = page.evaluate("""
            () => (
                localStorage.getItem('access') ||
                localStorage.getItem('token')  ||
                localStorage.getItem('auth')   ||
                ''
            )
        """).strip()
        if not token:
            raise RuntimeError("Токен не найден в localStorage. Убедитесь, что логин выполнен в этом же контексте.")
        scheme = "Bearer" if token.startswith("eyJ") else "Token"
        return token, scheme

    def build_headers(self, token: str, scheme: str) -> Dict[str, str]:
        return {
            "Authorization": f"{scheme} {token}",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": self.base,
            "Referer": self.base + "/",
        }

    def get_headers(self, page: Page, force_refresh: bool = False) -> Dict[str, str]:
        if self._headers is None or force_refresh:
            self.wait_token(page)
            token, scheme = self.extract_token_and_scheme(page)
            self._headers = self.build_headers(token, scheme)
        return dict(self._headers)