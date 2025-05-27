#!/usr/bin/env python3
"""
HTTP Web API version of Weather MCP Server
Railway.app için HTTP endpoint'li versiyon
"""

import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

# Flask uygulaması oluştur
app = Flask(__name__)

# OpenWeather API konfigürasyonu
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
OPENWEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather_data(city: str) -> dict:
    """OpenWeather API'den hava durumu verilerini al"""
    
    # API anahtarı kontrolü
    if not OPENWEATHER_API_KEY or OPENWEATHER_API_KEY == 'your_api_key_here':
        raise ValueError("API anahtarı bulunamadı. Lütfen OPENWEATHER_API_KEY environment variable'ını ayarlayın")
    
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

@app.route('/weather', methods=['GET'])
def get_weather():
    """
    Hava durumu bilgilerini dönen HTTP endpoint
    Query parametresi: city (zorunlu)
    """
    try:
        # Şehir parametresini al
        city = request.args.get('city')
        
        # Şehir parametresi kontrolü
        if not city:
            return jsonify({
                'error': 'Şehir parametresi gereklidir',
                'message': 'Lütfen city parametresini gönderin. Örnek: /weather?city=Istanbul'
            }), 400
        
        # Hava durumu verilerini al
        weather_data = get_weather_data(city)
        
        return jsonify(weather_data), 200
        
    except ValueError as e:
        return jsonify({
            'error': 'Hava durumu hatası',
            'message': str(e)
        }), 400
        
    except Exception as e:
        return jsonify({
            'error': 'Sunucu hatası',
            'message': f'Beklenmeyen bir hata oluştu: {str(e)}'
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """
    Servis sağlık kontrolü endpoint'i
    """
    return jsonify({
        'status': 'healthy',
        'service': 'Weather HTTP API',
        'version': '1.0.0',
        'api_key_configured': bool(OPENWEATHER_API_KEY and OPENWEATHER_API_KEY != 'your_api_key_here')
    }), 200

@app.route('/', methods=['GET'])
def home():
    """
    Ana sayfa - API kullanım bilgileri
    """
    return jsonify({
        'message': 'Hava Durumu HTTP API',
        'endpoints': {
            '/weather': 'GET - Hava durumu bilgisi (city parametresi gerekli)',
            '/health': 'GET - Servis sağlık kontrolü',
            '/': 'GET - Bu bilgi sayfası'
        },
        'example': '/weather?city=Istanbul',
        'documentation': 'city parametresi ile şehir adını gönderin'
    }), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🌤️ Hava Durumu HTTP API başlatılıyor...")
    print(f"📍 Port: {port}")
    print(f"🔗 Örnek kullanım: http://localhost:{port}/weather?city=Istanbul")
    print(f"🔑 API Key configured: {bool(OPENWEATHER_API_KEY and OPENWEATHER_API_KEY != 'your_api_key_here')}")
    
    app.run(host='0.0.0.0', port=port, debug=False)
