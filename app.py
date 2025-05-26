#!/usr/bin/env python3
"""
Hava Durumu MCP Server
OpenWeather API kullanarak hava durumu bilgilerini sağlayan MCP server
"""

import asyncio
import os
import sys
from typing import Any, Sequence
import requests
from dotenv import load_dotenv

from mcp.server import Server
from mcp import types

# .env dosyasını yükle
load_dotenv()

# OpenWeather API konfigürasyonu
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
OPENWEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# MCP Server oluştur
server = Server("weather-mcp-server")

async def get_weather_data(city: str) -> dict:
    """OpenWeather API'den hava durumu verilerini al"""

    # API anahtarı kontrolü
    if not OPENWEATHER_API_KEY or OPENWEATHER_API_KEY == 'your_api_key_here':
        raise ValueError("API anahtarı bulunamadı. Lütfen .env dosyasında OPENWEATHER_API_KEY değerini ayarlayın")

    # OpenWeather API'ye istek parametreleri
    params = {
        'q': city,
        'appid': OPENWEATHER_API_KEY,
        'units': 'metric',  # Celsius için
        'lang': 'tr'  # Türkçe açıklamalar için
    }

    try:
        # OpenWeather API'ye GET isteği gönder
        response = requests.get(OPENWEATHER_BASE_URL, params=params, timeout=10)

        # API yanıt kontrolü
        if response.status_code == 404:
            raise ValueError(f'"{city}" şehri bulunamadı. Lütfen geçerli bir şehir adı girin.')

        if response.status_code == 401:
            raise ValueError('OpenWeather API anahtarınız geçersiz. Lütfen kontrol edin.')

        if response.status_code != 200:
            raise ValueError(f'OpenWeather API hatası: {response.status_code}')

        # JSON verisini parse et
        weather_data = response.json()

        # Yanıt verisini formatla
        result = {
            'city': weather_data['name'],
            'country': weather_data['sys']['country'],
            'temperature': round(weather_data['main']['temp'], 1),
            'description': weather_data['weather'][0]['description'].title(),
            'humidity': weather_data['main']['humidity'],
            'wind_speed': weather_data['wind']['speed'],
            'pressure': weather_data['main']['pressure'],
            'feels_like': round(weather_data['main']['feels_like'], 1),
            'timestamp': weather_data['dt']
        }

        return result

    except requests.exceptions.Timeout:
        raise ValueError('API isteği zaman aşımına uğradı. Lütfen tekrar deneyin.')

    except requests.exceptions.ConnectionError:
        raise ValueError('API\'ye bağlanılamadı. İnternet bağlantınızı kontrol edin.')

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    MCP client'a mevcut araçları listele
    """
    return [
        types.Tool(
            name="get_weather",
            description="Belirtilen şehir için güncel hava durumu bilgilerini al",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "Hava durumu bilgisi alınacak şehir adı (örn: Istanbul, Ankara, London)"
                    }
                },
                "required": ["city"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    MCP client'dan gelen araç çağrılarını işle
    """
    if name != "get_weather":
        raise ValueError(f"Bilinmeyen araç: {name}")

    if not arguments or "city" not in arguments:
        raise ValueError("city parametresi gereklidir")

    city = arguments["city"]

    try:
        weather_data = await get_weather_data(city)

        # Sonucu formatla
        result_text = f"""🌤️ {weather_data['city']}, {weather_data['country']} Hava Durumu:

🌡️ Sıcaklık: {weather_data['temperature']}°C (Hissedilen: {weather_data['feels_like']}°C)
☁️ Durum: {weather_data['description']}
💧 Nem: {weather_data['humidity']}%
🌬️ Rüzgar: {weather_data['wind_speed']} m/s
📊 Basınç: {weather_data['pressure']} hPa

📅 Güncelleme: {weather_data['timestamp']}"""

        return [
            types.TextContent(
                type="text",
                text=result_text
            )
        ]

    except Exception as e:
        return [
            types.TextContent(
                type="text",
                text=f"❌ Hata: {str(e)}"
            )
        ]

async def main():
    # Stdin/stdout üzerinden MCP protokolü ile iletişim
    from mcp.server import stdio
    async with stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    print("🌤️ Hava Durumu MCP Server başlatılıyor...")
    print("📡 MCP protokolü ile iletişim kuruluyor...")
    asyncio.run(main())
