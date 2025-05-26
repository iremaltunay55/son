from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

app = Flask(__name__)

# OpenWeather API konfigürasyonu
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
OPENWEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

@app.route('/weather', methods=['GET'])
def get_weather():
    """
    Hava durumu bilgilerini dönen endpoint
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
        
        # API anahtarı kontrolü
        if not OPENWEATHER_API_KEY or OPENWEATHER_API_KEY == 'your_api_key_here':
            return jsonify({
                'error': 'API anahtarı bulunamadı',
                'message': 'Lütfen .env dosyasında OPENWEATHER_API_KEY değerini ayarlayın'
            }), 500
        
        # OpenWeather API'ye istek parametreleri
        params = {
            'q': city,
            'appid': OPENWEATHER_API_KEY,
            'units': 'metric',  # Celsius için
            'lang': 'tr'  # Türkçe açıklamalar için
        }
        
        # OpenWeather API'ye GET isteği gönder
        response = requests.get(OPENWEATHER_BASE_URL, params=params, timeout=10)
        
        # API yanıt kontrolü
        if response.status_code == 404:
            return jsonify({
                'error': 'Şehir bulunamadı',
                'message': f'"{city}" şehri bulunamadı. Lütfen geçerli bir şehir adı girin.'
            }), 404
        
        if response.status_code == 401:
            return jsonify({
                'error': 'API anahtarı geçersiz',
                'message': 'OpenWeather API anahtarınız geçersiz. Lütfen kontrol edin.'
            }), 401
        
        if response.status_code != 200:
            return jsonify({
                'error': 'API hatası',
                'message': f'OpenWeather API hatası: {response.status_code}'
            }), 500
        
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
        
        return jsonify(result), 200
        
    except requests.exceptions.Timeout:
        return jsonify({
            'error': 'Zaman aşımı',
            'message': 'API isteği zaman aşımına uğradı. Lütfen tekrar deneyin.'
        }), 408
        
    except requests.exceptions.ConnectionError:
        return jsonify({
            'error': 'Bağlantı hatası',
            'message': 'API\'ye bağlanılamadı. İnternet bağlantınızı kontrol edin.'
        }), 503
        
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
        'service': 'Weather MCP Service',
        'version': '1.0.0'
    }), 200

@app.route('/', methods=['GET'])
def home():
    """
    Ana sayfa - API kullanım bilgileri
    """
    return jsonify({
        'message': 'Hava Durumu MCP Servisi',
        'endpoints': {
            '/weather': 'GET - Hava durumu bilgisi (city parametresi gerekli)',
            '/health': 'GET - Servis sağlık kontrolü',
            '/': 'GET - Bu bilgi sayfası'
        },
        'example': '/weather?city=Istanbul',
        'documentation': 'city parametresi ile şehir adını gönderin'
    }), 200

if __name__ == '__main__':
    print("🌤️  Hava Durumu MCP Servisi başlatılıyor...")
    print("📍 Servis adresi: http://0.0.0.0:5000")
    print("🔗 Örnek kullanım: http://0.0.0.0:5000/weather?city=Istanbul")
    print("⚠️  .env dosyasında OPENWEATHER_API_KEY değerini ayarlamayı unutmayın!")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
