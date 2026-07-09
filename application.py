from flask import Flask, jsonify, request
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

LAT = -38.1
LON = 175.3

@app.route("/weather")
def weather():
    lat = request.args.get("lat", LAT)
    lon = request.args.get("lon", LON)

    url_forecast = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        "&hourly=temperature_2m,precipitation,uv_index"
        "&current_weather=true"
        "&timezone=auto"
    )

    url_nowcast = (
        "https://api.open-meteo.com/v1/nowcast"
        f"?latitude={lat}&longitude={lon}"
        "&precipitation=true"
        "&precipitation_probability=true"
        "&precipitation_type=true"
        "&timezone=auto"
    )

    raw_forecast = requests.get(url_forecast).json()
    raw_nowcast = requests.get(url_nowcast).json()

    hourly = raw_forecast.get("hourly", {})
    nowcast = raw_nowcast.get("nowcast", {})

    result = {
        "current": raw_forecast.get("current_weather", {}),
        "hourly": {
            "time": hourly.get("time", []),
            "temp": hourly.get("temperature_2m", []),
            "rain": hourly.get("precipitation", []),
            "uv": hourly.get("uv_index", []),
        },
        "minutely": {
            "time": nowcast.get("time", []),
            "rain": nowcast.get("precipitation", []),
            "prob": nowcast.get("precipitation_probability", []),
            "type": nowcast.get("precipitation_type", []),
        }
    }

    return jsonify(result)

@app.route("/ping")
def ping():
    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
