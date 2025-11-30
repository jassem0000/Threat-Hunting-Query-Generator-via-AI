@echo off
echo Installing Threat Hunting Query Generator Dependencies
echo ======================================================

echo Upgrading pip...
python -m pip install --upgrade pip

echo Installing dependencies from requirements.txt...
python -m pip install -r requirements.txt

if %errorlevel% == 0 (
    echo.
    echo Dependencies installed successfully!
    echo.
    echo To run the project:
    echo 1. Open a new terminal and run: cd backend ^&^& python manage.py migrate
    echo 2. Then run: python manage.py runserver
    echo 3. Open another terminal and run: streamlit run frontend/app.py
    echo.
    echo The application will be available at:
    echo - Backend API: http://localhost:8000
    echo - Frontend UI: http://localhost:8501
) else (
    echo.
    echo Installation failed. Trying individual package installation...
    echo.
    
    python -m pip install Django==4.2.7
    python -m pip install djangorestframework==3.14.0
    python -m pip install python-multipart==0.0.7
    python -m pip install streamlit==1.28.1
    python -m pip install requests==2.32.3
    python -m pip install ollama==0.5.3
    python -m pip install elasticsearch==8.10.1
    python -m pip install splunk-sdk==1.7.4
    python -m pip install stix2==3.0.1
    python -m pip install taxii2-client==2.3.0
    python -m pip install pandas==2.1.3
    python -m pip install numpy==1.26.4
    python -m pip install python-dotenv==1.0.0
    python -m pip install pyyaml==6.0.1
    python -m pip install pytest==7.4.3
    python -m pip install httpx==0.27.0
    python -m pip install plotly==5.18.0
    
    echo.
    echo Individual package installation completed!
    echo.
    echo To run the project:
    echo 1. Open a new terminal and run: cd backend ^&^& python manage.py migrate
    echo 2. Then run: python manage.py runserver
    echo 3. Open another terminal and run: streamlit run frontend/app.py
)

pause