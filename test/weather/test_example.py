from unittest.mock import patch, Mock
from weather.example import WeatherService, write_temperature, write_paris_temperature


def test_write_temperature():
    mock_ws = Mock()
    mock_ws.get_temperature.return_value = 16.1
    assert write_temperature(mock_ws, "Example city") == f"The temperature in Example city is 16.1°C"

@patch("weather.example.WeatherService._fetch_weather")
def test_get_temperature(mock_fetch):
    ws = WeatherService()
    mock_fetch.return_value = {'temperature': 16.1}
    assert ws.get_temperature(ws) == 16.1

# Test fails due to initialising WeatherService before patching
def test_patch_too_late():
    service = WeatherService()
    with patch.object(WeatherService, 'choose_base_url', return_value="test-url"):
        assert service.base_url == "test-url"  # Patch has no effect

# Last test assertion fails because the mock attribute is set after the call to the tested method
@patch("weather.example.WeatherService._fetch_weather", return_value=None)
@patch("weather.example.WeatherService._parse_temperature", return_value=25)
def test_modify_mock_after_call(mock_parse, mock_fetch):
    service = WeatherService()
    result = service.get_temperature("London")
    mock_parse.return_value = 30
    mock_fetch.assert_called_once()
    assert result == 30

# This test fails because when we are patching the WeatherService class, not an instance of it
@patch("weather.example.WeatherService", autospec=True)
def test_patch_class_but_real_instance_used(mock_service):
    mock_service.get_temperature.return_value = 18
    assert write_paris_temperature() == "The temperature in Paris is 18°C"

# This is a direct fix for the above issues
@patch("weather.example.WeatherService", autospec=True)
def test_patch_class_mock(mock_service):
    mock_ws = Mock()
    mock_ws.get_temperature.return_value = 18
    mock_service.return_value = mock_ws
    assert write_paris_temperature() == "The temperature in Paris is 18°C"

# This is the easiest way to patch an instance method
@patch.object(WeatherService, 'get_temperature', autospec=True, return_value=18)
def test_patch_class_mock_object():
    assert write_paris_temperature() == "The temperature in Paris is 18°C"
