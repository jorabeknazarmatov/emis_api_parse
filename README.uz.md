# ⚙️ Emis API Exporter

🇬🇧 [English](README.md) • 🇷🇺 [Русский](README.ru.md) • 🇺🇿 Oʻzbekcha

EMIS veb-API дан talaba, o‘qituvchi va semestr ma’lumotlarini chiqarib olish va natijani lokal JSON faylga saqlash uchun kichik Python utilitasi.

## Tez boshlash

1) Virtual muhitni yaratish va faollashtirish (PowerShell)

```powershell
python -m venv .venv
# PowerShell da faollashtirish
.\.venv\Scripts\Activate.ps1
```

Agar cmd.exe ishlatadigan bo‘lsangiz:

```cmd
.venv\Scripts\activate.bat
```

2) Bog‘lanmalarni o‘rnatish

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
# Playwright brauzerlarini bir marta o‘rnatish
python -m playwright install
```

3) `.env` sozlamalari

Loyihaning ildizida `.env` faylini yarating va quyidagilarni qo‘shing:

```dotenv
ONEID_LOGIN=your_login_here
ONEID_PASSWORD=your_password_here
```

Ushbu o‘zgaruvchilar `python-dotenv` orqali yuklanadi (qarang `core/config.py`). `main.py` ni ishga tushirayotgan katalogga `.env` joylashtiring (odatda loyihaning ildizi).

4) O'quv reja JSON fayllarini joylashtiring

Iltimos, quyidagi fayllar `main.py` bilan birga loyihaning ildizida bo‘lsin:

- `feldsherlik_ishi.json`
- `hamshiralik_ishi.json`

Ushbu fayllar eksport jarayonida kirish sifatida ishlatiladi.

5) Ishga tushirish

```powershell
python main.py
```

6) Natija

Muvaffaqiyatli bajarilganda `all_students.json` fayli loyihaning ildiziga yoziladi.

## Eslatma / Notes / Примечание

- ▶️ Agar Playwright brauzerlar yetishmasa, `python -m playwright install chromium` yoki `python -m playwright install --with-deps` buyrug‘ini bajaring.
- 🧩 OneID sessiyasi va cookie holati `oneid_state.json` da saqlanadi — bu qayta avtorizatsiyadan qochishga yordam beradi.
- 📦 Diagnostika uchun `core/logger.py` orqali chiqariladigan loglarni kuzatib boring.
- 🔒 `.env` faylini versiyalashga qo‘shmang. Kerak bo‘lsa `.gitignore` ga qo‘shing.

---

MIT © Turabek
