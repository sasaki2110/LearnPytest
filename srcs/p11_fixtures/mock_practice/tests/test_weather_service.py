"""
天気サービスのテスト
外部API呼び出しをモック化してテストします。
"""

import pytest
from unittest.mock import Mock, patch
from services.weather_service import WeatherService


@pytest.fixture
def weather_service():
    """天気サービスのフィクスチャ"""
    return WeatherService(api_key="test_api_key")


@pytest.fixture
def mock_requests_get():
    """requests.get をモック化するフィクスチャ"""
    with patch("services.weather_service.requests.get") as mock_get:
        yield mock_get


def test_get_weather_success(weather_service, mock_requests_get):
    """天気情報の取得が成功する場合のテスト"""
    # モックの戻り値を設定
    mock_response = Mock()
    mock_response.json.return_value = {
        "city": "Tokyo",
        "temperature": 25,
        "condition": "Sunny"
    }
    mock_response.raise_for_status = Mock()  # エラーを発生させない
    mock_requests_get.return_value = mock_response
    
    # テスト実行
    result = weather_service.get_weather("Tokyo")
    
    # 結果を検証
    assert result["city"] == "Tokyo"
    assert result["temperature"] == 25
    assert result["condition"] == "Sunny"
    
    # APIが正しく呼ばれたことを確認
    mock_requests_get.assert_called_once()
    call_args = mock_requests_get.call_args
    assert call_args[1]["params"]["city"] == "Tokyo"
    assert call_args[1]["params"]["api_key"] == "test_api_key"


def test_get_forecast(weather_service, mock_requests_get):
    """天気予報の取得テスト"""
    # モックの戻り値を設定
    mock_response = Mock()
    mock_response.json.return_value = {
        "forecast": [
            {"day": 1, "temperature": 25, "condition": "Sunny"},
            {"day": 2, "temperature": 23, "condition": "Cloudy"},
            {"day": 3, "temperature": 22, "condition": "Rainy"}
        ]
    }
    mock_response.raise_for_status = Mock()
    mock_requests_get.return_value = mock_response
    
    # テスト実行
    result = weather_service.get_forecast("Tokyo", days=3)
    
    # 結果を検証
    assert len(result) == 3
    assert result[0]["day"] == 1
    assert result[0]["temperature"] == 25
    assert result[2]["condition"] == "Rainy"
    
    # APIが正しく呼ばれたことを確認
    call_args = mock_requests_get.call_args
    assert call_args[1]["params"]["days"] == 3


def test_get_weather_api_error(weather_service, mock_requests_get):
    """APIエラーが発生する場合のテスト"""
    # モックでエラーを発生させる
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = Exception("API Error")
    mock_requests_get.return_value = mock_response
    
    # エラーが発生することを確認
    with pytest.raises(Exception, match="API Error"):
        weather_service.get_weather("Tokyo")

