@echo off
echo Threat Hunting Query Generator
echo ==============================

echo Installing dependencies...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo Dependency installation failed. Trying alternative approach...
    python install_deps.py
)

echo Setting up Django...
cd backend
python manage.py migrate

if %errorlevel% neq 0 (
    echo Django setup failed. Please check the error messages above.
    pause
    exit /b 1
)

echo Starting Django backend server...
start cmd /k "python manage.py runserver"

cd ..

echo Starting Streamlit frontend...
start cmd /k "streamlit run frontend/app.py"

echo.
echo Project started successfully!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:8501
echo.
pause