"""
天気情報を取得するサービス
外部APIを呼び出して天気情報を取得します。
"""

import requests


class WeatherService:
    """天気情報を取得するサービスクラス"""
    
    def __init__(self, api_key: str):
        """
        初期化
        
        Args:
            api_key: 天気APIのキー
        """
        self.api_key = api_key
        self.base_url = "https://api.weather.example.com"
    
    def get_weather(self, city: str) -> dict:
        """
        指定した都市の天気情報を取得
        
        Args:
            city: 都市名
            
        Returns:
            天気情報の辞書
            {
                "city": "Tokyo",
                "temperature": 25,
                "condition": "Sunny"
            }
        """
        url = f"{self.base_url}/weather"
        params = {
            "city": city,
            "api_key": self.api_key
        }
        
        # 外部APIを呼び出し
        response = requests.get(url, params=params)
        response.raise_for_status()  # エラーがあれば例外を発生
        
        data = response.json()
        
        return {
            "city": data.get("city"),
            "temperature": data.get("temperature"),
            "condition": data.get("condition")
        }
    
    def get_forecast(self, city: str, days: int = 3) -> list:
        """
        指定した都市の天気予報を取得
        
        Args:
            city: 都市名
            days: 予報日数（デフォルト: 3日）
            
        Returns:
            天気予報のリスト
        """
        url = f"{self.base_url}/forecast"
        params = {
            "city": city,
            "days": days,
            "api_key": self.api_key
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        return response.json().get("forecast", [])

