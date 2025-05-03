from unittest.mock import patch, Mock
from weather.example import WeatherService, write_temperature

def test_write_temperature():
    mock_ws = Mock()
    mock_ws.get_temperature.return_value = 16.1
    assert write_temperature(mock_ws, "Example city") == f"The temperature in Example city is 16.1°C"

@patch("weather.example.WeatherService._fetch_weather")
def test_get_temperature(mock_fetch):
    ws = WeatherService()
    mock_fetch.return_value = {'temperature': 16.1}
    assert ws.get_temperature(ws) == 16.1

def test_patch_too_late():
    service = WeatherService()
    with patch.object(WeatherService, 'choose_base_url', return_value="test-url"):
        assert service.base_url == "test-url"  # Patch has no effect

@patch("weather.example.WeatherService._parse_temperature", return_value=25)
def test_modify_mock_after_call(mock_parse):
    service = WeatherService()
    result = service.get_temperature("London")
    mock_parse.return_value = 30 
    assert result == 25

@patch("weather.example.WeatherService", autospec=True)
def test_patch_class_but_real_instance_used(mock_service_class):
    real_service = WeatherService()
    with patch.object(real_service, "_fetch_weather", return_value={"temperature": 18}):
        assert write_temperature(real_service, "Paris") == "The temperature in Paris is 18°C"

@patch("weather.example.WeatherService._fetch_weather", return_value={"temperature": 22})
def test_patch_private_method(mock_fetch):
    service = WeatherService()
    temp = service.get_temperature("Berlin")
    assert temp == 22
    mock_fetch.assert_called_once_with("Berlin")
