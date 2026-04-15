@echo off
echo Starting CPU Scheduling Simulator...
cd backend

echo Installing Python requirements...
pip install -r requirements.txt

echo.
echo Starting Flask Server on http://127.0.0.1:5000
echo Press Ctrl+C to stop.
echo.

python app.py
pause
