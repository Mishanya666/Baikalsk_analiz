import requests
import pandas as pd

# Координаты Байкальска
latitude = 51.5211
longitude = 104.1496

start_date = "2020-01-01"
end_date = "2025-01-01"

# Open-Meteo API
url = "https://archive-api.open-meteo.com/v1/archive"
params = {
    "latitude": latitude,
    "longitude": longitude,
    "start_date": start_date,
    "end_date": end_date,
    "daily": [
        "temperature_2m_max",
        "temperature_2m_min",
        "precipitation_sum",
        "windspeed_10m_max",
        "winddirection_10m_dominant",
        "sunshine_duration"
    ],
    "timezone": "Asia/Irkutsk"
}

# Запрос к API
response = requests.get(url, params=params)
data = response.json()

# Преобразование в DataFrame
df = pd.DataFrame({
    "date": data["daily"]["time"],
    "temp_max": data["daily"]["temperature_2m_max"],
    "temp_min": data["daily"]["temperature_2m_min"],
    "precip_mm": data["daily"]["precipitation_sum"],
    "wind_max_mps": data["daily"]["windspeed_10m_max"],
    "wind_dir_deg": data["daily"]["winddirection_10m_dominant"],
    "sunshine_hours": [round(x / 3600, 2) if x is not None else None for x in data["daily"]["sunshine_duration"]]
})

df.to_csv("baikal_weather_summer2020-2025.csv", index=False)
print("✅ Данные сохранены в baikal_weather_summer2020-2025.csv")
