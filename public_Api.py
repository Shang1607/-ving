import streamlit as st
import requests

API_KEY = 'df4119fcde18c1eb7d3885a0129b4724'

def public_Api():
    # Function to set background image
    def add_bg_image(image_url):
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("{image_url}");
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

    # Call the function with a default background image
    add_bg_image("https://example.com/default_weather.jpg")

    st.title('Enhanced Weather App')

    # User input for city
    city = st.text_input('Enter a city')

    if city:
        try:
            # API call
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
            with st.spinner('Fetching data...'):
                response = requests.get(url)
                response.raise_for_status()

            # Process API response
            data = response.json()
            temperature_kelvin = data['main']['temp']
            temperature_celsius = temperature_kelvin - 273.15
            temperature_fahrenheit = (temperature_kelvin - 273.15) * 9/5 + 32
            humidity = data['main']['humidity']
            condition = data['weather'][0]['description']

            # Toggle for temperature unit
            unit = st.radio("Select temperature unit:", ["Celsius (°C)", "Fahrenheit (°F)"])
            if unit == "Celsius (°C)":
                temperature = temperature_celsius
            else:
                temperature = temperature_fahrenheit

            # Update background image based on condition
            if "clear" in condition.lower():
                add_bg_image("https://example.com/sunny.jpg")
            elif "cloud" in condition.lower():
                add_bg_image("https://example.com/cloudy.jpg")
            elif "rain" in condition.lower():
                add_bg_image("https://example.com/rainy.jpg")

            # Display weather details
            st.write(f'### Weather in {city.capitalize()}')
            st.write(f'- **Temperature**: {temperature:.2f} {unit.split()[0]}')
            st.write(f'- **Humidity**: {humidity}%')
            st.write(f'- **Condition**: {condition.capitalize()}')
        except requests.exceptions.HTTPError:
            st.error("City not found. Please enter a valid city name.")
        except requests.exceptions.RequestException:
            st.error("Unable to connect to the weather service. Please try again later.")
