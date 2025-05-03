import requests

class WeatherService:
    def __init__(self, base_url=None):
        self.default_url = "https://example.weather.api"
        self.base_url = self.choose_base_url(base_url)

    def choose_base_url(self, base_url):
        if base_url is None:
            return self.default_url
        return base_url

    def get_temperature(self, city):
        raw_data = self._fetch_weather(city)
        return self._parse_temperature(raw_data)

    def _fetch_weather(self, city):
        response = requests.get(f"{self.base_url}/weather/{city}")
        response.raise_for_status()
        return response.json()

    @staticmethod
    def _parse_temperature(data):
        return data["temperature"]

def write_temperature(service: WeatherService, city):
    temp = service.get_temperature(city)
    return f"The temperature in {city} is {temp}°C"
