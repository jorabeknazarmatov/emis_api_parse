# ⚙️ Emis API Exporter

🇺🇸 [English](README.md) • 🇷🇺 Русский • [Oʻzbekcha](README.uz.md) 🇺🇿

Небольшая утилита на Python для экспорта данных студентов, преподавателей и семестров из EMIS API и сохранения результата в локальном JSON-файле.

## Быстрый старт

1) Создайте и активируйте виртуальное окружение (PowerShell)

```powershell
python -m venv .venv
# активировать в PowerShell
.\.venv\Scripts\Activate.ps1
```

Если вы используете cmd.exe:

```cmd
.venv\Scripts\activate.bat
```

2) Установите зависимости

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
# Установите браузеры Playwright (один раз)
python -m playwright install
```

3) Настройка `.env`

Создайте файл `.env` в корне проекта и добавьте переменные:

```dotenv
ONEID_LOGIN=your_login_here
ONEID_PASSWORD=your_password_here
```

Проект загружает эти переменные через `python-dotenv` (см. `core/config.py`). Поместите `.env` в директорию, из которой вы запускаете `main.py` (обычно корень проекта).

4) Поместите учебные планы

Убедитесь, что в корне проекта рядом с `main.py` лежат:

- `feldsherlik_ishi.json`
- `hamshiralik_ishi.json`

Эти файлы используются в качестве входных учебных планов при экспорте.

5) Запуск

```powershell
python main.py
```

6) Результат

Данные будут сохранены в `all_students.json` в корне проекта.

## Примечание / Notes / Eslatma

- ▶️ Если Playwright сообщает об отсутствии браузеров, выполните `python -m playwright install chromium` или `python -m playwright install --with-deps`.
- 🧩 Состояние сессии OneID сохраняется в `oneid_state.json` — удобно для избежания повторной авторизации.
- 📦 Логи пишутся через `core/logger.py` — смотрите вывод в консоли для диагностики.
- 🔒 Не коммитьте `.env` в репозиторий. Добавьте его в `.gitignore`, если нужно.

---

MIT © Turabek
