from flask import Flask, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

LAT = -38.1
LON = 175.3

@app.route("/weather")
def weather():
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={LAT}&longitude={LON}"
        "&hourly=temperature_2m,precipitation,uv_index"
        "&current_weather=true"
    )

    raw = requests.get(url).json()

    result = {
        "current": raw.get("current_weather", {}),
        "minutely": {
            "time": raw["minutely"]["time"],
            "temp": raw["minutely"]["temperature_2m"],
            "rain": raw["minutely"]["precipitation"],
            "uv": raw["minutely"]["uv_index"],
        }
    }

    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)