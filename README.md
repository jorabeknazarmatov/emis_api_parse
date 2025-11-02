# Playwright authentication helper

This script automates login to OneID and saves Playwright storage state (cookies/localStorage) to the path defined in `core.config.STATE_PATH`.

Prerequisites
- Python and a virtual environment (recommended)
- `requirements.txt` in project root contains `playwright` and `dotenv`

Install dependencies (PowerShell):

```powershell
python -m pip install -r requirements.txt
python -m playwright install
```

How to run

Run the auth script as a module so imports (like `core.config`) work from project root:

```powershell
python -m app.auth.auth
```

Notes
- The script will first attempt automated fill+submit using common selectors. If that fails, it will open a headed browser and wait for you to complete login manually. After a successful redirect to the configured target URL, it saves storage state to the file referenced by `core.config.STATE_PATH` (by default `oneid_state.json`).
- Ensure your `.env` contains `ONEID_LOGIN` and `ONEID_PASSWORD`.
