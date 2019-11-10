#!/bin/bash

# Setup script to make sure dependencies are installed and run the app

echo "Installing pip dependencies..."

pip install poloniex krakenex flask datetime

echo "Running app..."
cd code
FLASK_APP=/code/main.py flask run --host=0.0.0.0