from flask import Flask, render_template, request
from dotenv import load_dotenv
import requests
import os

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    error = None
    forecast = []
    if request.method == "POST":
        city = request.form.get("city")
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()
        if data["cod"] == 200:
            weather = {
                "city": data["name"],
                "temp": data["main"]["temp"],
                "description": data["weather"][0]["description"],
                "humidity": data["main"]["humidity"],
                "wind": data["wind"]["speed"]
            }
            forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric&cnt=40"
            forecast_response = requests.get(forecast_url)
            forecast_data = forecast_response.json()
            forecast = []
            seen_dates = []
            for item in forecast_data["list"]:
                date = item["dt_txt"].split(" ")[0]
                if date not in seen_dates:
                    seen_dates.append(date)
                    forecast.append({
                        "date": date,
                        "temp": item["main"]["temp"],
                        "description": item["weather"][0]["description"]
                    })
                if len(forecast) == 5:
                    break
        else:
            error = "City not found!"
    return render_template("index.html", weather=weather, error=error, forecast=forecast)

if __name__ == "__main__":
    app.run(debug=True)
