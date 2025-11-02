# 🇺🇿 Emis API Exporter

Choose your language:
| Language | File |
|-----------|------|
<!-- Primary README (English). Other languages: README.ru.md, README.uz.md -->
# ⚙️ Emis API Exporter

�� English • [Русский](README.ru.md) �� • [Oʻzbekcha](README.uz.md) 🇺🇿

A small, focused Python utility to export student, teacher and semester data from the EMIS web API and save it to a local JSON file.

## Quick start

1) Create and activate a virtual environment (PowerShell)

```powershell
python -m venv .venv
# activate in PowerShell
.\.venv\Scripts\Activate.ps1
```

If you prefer cmd.exe:

```cmd
.venv\Scripts\activate.bat
```

2) Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
# Install Playwright browsers (one-time)
python -m playwright install
```

3) Configure `.env`

Create a file named `.env` in the project root and add the following variables:

```dotenv
ONEID_LOGIN=your_login_here
ONEID_PASSWORD=your_password_here
```

The project reads these values via `python-dotenv` (see `core/config.py`). Place `.env` in the same directory from which you run `main.py` (project root by default).

4) Place curriculum JSON files

Ensure the following files are present in the project root next to `main.py`:

- `feldsherlik_ishi.json`
- `hamshiralik_ishi.json`

These files are used as curriculum input during export.

5) Run the exporter

```powershell
python main.py
```

6) Output

On success, the exporter writes results to `all_students.json` in the project root.

## Notes / Примечание / Eslatma

- ▶️ If Playwright complains about missing browsers, run `python -m playwright install chrominum` or `python -m playwright install --with-deps`.
- 🧩 Session and cookie state for OneID is saved to `oneid_state.json` (useful to avoid repeated logins).
- 📦 Logs are produced by `core/logger.py` — check console output for diagnostics and progress.
- 🔒 Keep your `.env` out of version control. Add it to `.gitignore` if necessary.

---

## License

MIT © Turabek
