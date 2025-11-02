# 🇺🇿 Emis API Exporter

Tilni tanlang:
| Til | Fayl |
|-----|------|
| 🇬🇧 English | [Read in English](README.md) |
| 🇷🇺 Русский | [Читать по-русски](README.ru.md) |
| 🇺🇿 O‘zbekcha | Siz hozir shu tildasiz |

---

## 📖 Loyihaning maqsadi
Ushbu loyiha Playwright va Python yordamida Emis ta’lim platformasidan ma’lumotlarni avtomatik eksport qiladi.

### 🔧 O‘rnatish (Windows PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m playwright install
```

### ⚙️ Muhit o‘zgaruvchilari
Root papkada `.env` fayl yarating:
```
ONEID_LOGIN=sizning_login
ONEID_PASSWORD=sizning_parol
```

### ▶️ Ishga tushirish
```powershell
python main.py
```

### 🗂 Natija
Barcha o‘quvchilar `all_students.json` fayliga saqlanadi.

---

## 🧩 Eslatma
- Muhit sozlamalari `dotenv` orqali yuklanadi.
- Brauzer avtomatizatsiyasi `Playwright` orqali bajariladi.
- Log yozuvlari `core/logger.py` orqali ko‘rsatiladi.
