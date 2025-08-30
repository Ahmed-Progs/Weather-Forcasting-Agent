import streamlit as st
import requests

# App title
st.set_page_config(page_title="Weather Forecasting App", page_icon="🌦️")
st.title("🌦️ Weather Forecasting App")

# User input for city
city = st.text_input("Enter city name:", "London")

if st.button("Get Weather"):
    if not city.strip():
        st.error("Please enter a city name.")
    else:
        try:
            # Step 1: Get coordinates from city name using Nominatim (OpenStreetMap)
            geo_url = f"https://nominatim.openstreetmap.org/search?city={city}&format=json"
            geo_resp = requests.get(geo_url, headers={"User-Agent": "streamlit-app"}).json()

            if isinstance(geo_resp, list) and len(geo_resp) > 0:
                lat = geo_resp[0]["lat"]
                lon = geo_resp[0]["lon"]

                # Step 2: Get weather data from Open-Meteo (no API key required)
                weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
                weather_resp = requests.get(weather_url).json()

                if "current_weather" in weather_resp:
                    data = weather_resp["current_weather"]

                    # Display results
                    st.subheader(f"Weather in {city.title()}")
                    st.metric("🌡️ Temperature", f"{data['temperature']} °C")
                    st.write(f"💨 Wind Speed: {data['windspeed']} km/h")
                    st.write(f"⏱️ Time: {data['time']}")
                else:
                    st.error("Weather data not available for this location.")
            else:
                st.error("City not found in geocoding service.")
        
        except Exception as e:
            st.error(f"Error fetching data: {e}")
