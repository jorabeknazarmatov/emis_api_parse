# Emis API Exporter

Инструкция по установке и запуску (Windows PowerShell).

1) Установка виртуального окружения (venv)

Откройте PowerShell в корне проекта и выполните:

```powershell
python -m venv .venv
# Активировать в PowerShell
.\.venv\Scripts\Activate.ps1
```

Если используете cmd.exe:

```cmd
.venv\Scripts\activate.bat
```

2) Установка зависимостей

После активации venv установите зависимости:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
# Установите браузеры для Playwright (один раз)
python -m playwright install
```

3) Заполнить `.env`

В проекте используется dotenv. В `core/config.py` требуются переменные:

- ONEID_LOGIN
- ONEID_PASSWORD

Скопируйте пример (если есть) и создайте `.env` в корне проекта или создайте файл `.env` в корне со следующими строками:

```
ONEID_LOGIN=your_login_here
ONEID_PASSWORD=your_password_here
```

Примечание: `load_dotenv()` ищет `.env` в текущей рабочей директории. Если вы запускаете `main.py` из корня проекта — положите `.env` в корень.

4) Положите в корень проекта файлы учебных планов

Убедитесь, что файлы `feldsherlik_ishi.json` и `hamshiralik_ishi.json` находятся в корне проекта (рядом с `main.py`). Эти файлы используются как входные учебные планы.

5) Запуск

Активируйте venv (см. шаг 1) и запустите:

```powershell
python main.py
```

6) Результаты

После успешного выполнения данные будут сохранены в `all_students.json` в корне проекта.

Дополнительно / отладка

- Если Playwright жалуется на браузеры, выполните `python -m playwright install chromium` или `python -m playwright install --with-deps`.
- Файл состояния для OneID хранится в `oneid_state.json` (используется для cookies/storage).
- Логирование выводится через `core/logger.py` — смотрите вывод в консоли для диагностики.

Если нужно, могу добавить пример `.env.example` в корень или автоматический скрипт для создания venv и установки зависимостей.

