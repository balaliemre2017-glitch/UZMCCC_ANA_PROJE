@echo off
chcp 65001 >nul
title V26 TAM OTOMATIK - KANKA BEKLE
echo === V26 TAM OTOMATIK KURULUYOR ===
cd /d C:\UZMCCC_ANA_PROJE\UZMCCC_ANA_PROJE
echo Eski Turkce klasorler siliniyor...
for %%D in (uygulama yetkilendirme yapilandirma cekirdek veritabani "baslangic asamasi" panel yuklemeler isciler "daha iyi" ler_yedekleme) do rmdir /s /q "%%D" 2>nul
del /f /q 0_PROJE_HAFIZASI_ASLA_SILME.md 2>nul
del /f /q yedekler\uzmccc.db 2>nul

echo Zip araniyor...
set ZIP1=C:\UZMCCC_ANA_PROJE\UZMCCC_V26_TAM_OTOMATIK_SOSYAL_BOT_1.zip
set ZIP2=%USERPROFILE%\Downloads\UZMCCC_V26_TAM_OTOMATIK_SOSYAL_BOT_1.zip
set ZIP3=%USERPROFILE%\Indirilenler\UZMCCC_V26_TAM_OTOMATIK_SOSYAL_BOT_1.zip

if exist "%ZIP1%" set FOUND=%ZIP1%
if exist "%ZIP2%" set FOUND=%ZIP2%
if exist "%ZIP3%" set FOUND=%ZIP3%

if "%FOUND%"=="" (
  echo ZIP BULUNAMADI!
  echo Lutfen V26 zip'i C:\UZMCCC_ANA_PROJE klasorune koy!
  pause
  exit /b
)

echo Bulundu: %FOUND%
echo Aciliyor...
powershell -Command "Expand-Archive -Force '%FOUND%' 'C:\UZMCCC_ANA_PROJE\temp_v26'"

xcopy /E /Y /Q "C:\UZMCCC_ANA_PROJE\temp_v26\*" "C:\UZMCCC_ANA_PROJE\UZMCCC_ANA_PROJE\"
rmdir /s /q "C:\UZMCCC_ANA_PROJE\temp_v26" 2>nul

echo GitHub'a gonderiliyor...
git add -A
git commit -m "V26 GERCEK - core workers main.py - tam otomatik"
git push -u origin ana --force

echo.
echo ===== BITTI KANKA! =====
echo GitHub: https://github.com/balaliemre2017-glitch/UZMCCC_ANA_PROJE
echo Simdi botu baslat: python main.py
pause
