# 🇺🇿 Emis API Exporter

Choose your language:
| Language | File |
|-----------|------|
| 🇬🇧 English | You are here |
| 🇷🇺 Русский | [Читать по-русски](README.ru.md) |
| 🇺🇿 Oʻzbekcha | [O‘qish o‘zbek tilida](README.uz.md) |

---

## 📖 Description
This project automates data export from the Emis educational platform using Playwright and Python.

### 🔧 Installation (Windows PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m playwright install
```

### ⚙️ Environment Variables
Create a `.env` file in the root:
```
ONEID_LOGIN=your_login
ONEID_PASSWORD=your_password
```

### ▶️ Run
```powershell
python main.py
```

### 🗂 Output
Results are saved to `all_students.json` in the root directory.

---

## 🧩 Notes
- Uses `dotenv` for environment variables.
- Uses `Playwright` for browser automation.
- Logs are handled via `core/logger.py`.
