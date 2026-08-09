@echo off
cd /d "%~dp0"
set PYTHONPATH=%cd%
python -c "from database.models import init_db; init_db()"
python -m panel.app
pause
