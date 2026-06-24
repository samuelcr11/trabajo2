#!/bin/bash
set -e

echo "Installing dependencies..."
cd backend
pip install --upgrade pip
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --noinput || true

echo "Build completed successfully!"
