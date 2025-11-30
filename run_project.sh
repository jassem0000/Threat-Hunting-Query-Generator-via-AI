#!/bin/bash

echo "Threat Hunting Query Generator"
echo "=============================="

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Setting up Django..."
cd backend
python manage.py migrate

echo "Starting Django backend server..."
gnome-terminal -- python manage.py runserver &

cd ..

echo "Starting Streamlit frontend..."
gnome-terminal -- streamlit run frontend/app.py &

echo ""
echo "Project started successfully!"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:8501"
echo ""