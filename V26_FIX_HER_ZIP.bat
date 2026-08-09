@echo off
chcp 65001 >nul
title V26 FIX - HER ZIP'I BULUR
cd /d C:\UZMCCC_ANA_PROJE\UZMCCC_ANA_PROJE
echo === ESKI TURKCE KLASORLER SILINIYOR ===
for %%D in (uygulama yetkilendirme yapilandirma cekirdek veritabani "baslangic asamasi" panel yuklemeler isciler "daha iyi" ler_yedekleme) do rmdir /s /q "%%D" 2>nul

echo Zip araniyor...
set FOUND=
for %%F in (*V26*.zip) do set FOUND=%%F
if "%FOUND%"=="" for %%F in (C:\UZMCCC_ANA_PROJE\*V26*.zip) do set FOUND=%%F

if "%FOUND%"=="" (
  echo ZIP BULUNAMADI! Lutfen zip'i bu klasore koy!
  pause
  exit /b
)

echo Bulundu: %FOUND%
echo Aciliyor...
powershell -Command "Expand-Archive -Force '%FOUND%' 'C:\UZMCCC_ANA_PROJE\temp_v26'"

echo Kopyalaniyor...
xcopy /E /Y /Q "C:\UZMCCC_ANA_PROJE\temp_v26\*" "C:\UZMCCC_ANA_PROJE\UZMCCC_ANA_PROJE\" 2>nul
if exist "C:\UZMCCC_ANA_PROJE\temp_v26\UZMCCC_ANA_PROJE" xcopy /E /Y /Q "C:\UZMCCC_ANA_PROJE\temp_v26\UZMCCC_ANA_PROJE\*" "C:\UZMCCC_ANA_PROJE\UZMCCC_ANA_PROJE\"
rmdir /s /q "C:\UZMCCC_ANA_PROJE\temp_v26" 2>nul

echo GitHub'a gonderiliyor...
git add -A
git commit -m "V26 GERCEK BOT - core workers main.py"
git push -u origin ana --force

echo.
echo === BITTI KANKA ===
echo core klasoru var mi kontrol et:
dir /b
pause
