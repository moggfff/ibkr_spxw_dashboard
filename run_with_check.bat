@echo off
echo Starting IBKR Dashboard...

REM تفعيل البيئة الافتراضية
call .\.venv\Scripts\activate

REM تحديد متغيرات البيئة الخاصة بـ Flask
set FLASK_APP=main.py
set FLASK_ENV=development

REM تشغيل السيرفر على المنفذ 7860
flask run --host=127.0.0.1 --port=7860

pause
