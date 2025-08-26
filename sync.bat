@echo off
REM === 1) اذهب إلى مجلد المشروع ===
cd /d C:\Users\TOSHIBA\Desktop\fax\ibkr_spxw_dashboard

REM === 2) اجلب آخر تغييرات بدون إنشاء Merge عشوائي ===
git pull --rebase --autostash origin main

REM === 3) أضف أي تغييرات محلية ===
git add -A

REM === 4) إن وُجدت تغييرات مضافة، اعمل Commit تلقائي ===
git diff --cached --quiet || git commit -m "Auto-sync %DATE% %TIME%"

REM === 5) ادفع التغييرات إلى GitHub ===
git push origin main
