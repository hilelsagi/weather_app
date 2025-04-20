
# 🌤️ Python Weather App

A simple containerized Python application that provides real-time weather information for any city using an API (Open-Meteo API).
This project is using an object oriented approach for handling and parsing the weather data.

## 🚀 Features

- Get current weather for any city using search bar
- Get current weather for popular big cities using city buttons
- Displays daytime & nighttime weather, and avarage humidity
- Clean and easy-to-use interface (CLI/GUI/Web)
- Real-time data from a free public weather API


## 🛠️ Technologies Used

- Python 3
- Flask
- Open-Meteo API
- Docker & docker-compose 

## 📦 Installation

git clone https://github.com/hilelsagi/weather_app.git
cd weather_app

(Optional) Create a virtual environment:

python -m venv venv
source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Run:

python3 app.py

Using docker-compse (make sure you have docker-compose installed):


git clone https://github.com/hilelsagi/weather_app.git
cd weather_app
docker-compose up -d


Access the app on your browser at http://localhost:5000/



