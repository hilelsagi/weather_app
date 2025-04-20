import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, request
from backend.get_weather_data import get_weather_data

app = Flask(__name__)
#logging configuration
log_handler = RotatingFileHandler(
    "logs/app.log",  # Log file path
    maxBytes=5000000,  # 5MB per log file
    backupCount=5,  # Keep up to 5 old log files
    encoding="utf-8"
)
log_handler.setLevel(logging.INFO)
log_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
log_handler.setFormatter(log_formatter)
app.logger.addHandler(log_handler)

@app.route("/", methods=["GET", "POST"])
def index():
    """Handles city input and displays weather or error messages."""
    if request.method == "POST":
        city = request.form.get("city", "").strip()

        if not city:
            app.logger.warning("User submitted an empty city name.")
            return render_template("index.html", error="Please enter a city name.")

        try:
            weather_data = get_weather_data(city)
            app.logger.info(f"Weather data successfully retrieved for city: {city}")
            return render_template("index.html", weather=weather_data, city=city)

        except (ValueError, RuntimeError, ConnectionError) as e:
            app.logger.error(f"Error occurred: {str(e)}")
            return render_template("index.html", error=str(e))  

        except Exception as e:
            app.logger.critical(f"Unexpected error: {str(e)}", exc_info=True)
            return render_template("index.html", error="An unexpected error occurred. Please try again later.")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
