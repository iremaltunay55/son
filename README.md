# Hava Durumu MCP Servisi

Python Flask kullanarak geliştirilmiş basit bir hava durumu MCP (Model Context Protocol) servisi.

## Özellikler

- OpenWeather API'den gerçek zamanlı hava durumu verileri
- RESTful API endpoint'leri
- JSON formatında yanıtlar
- Hata yönetimi ve validasyon
- Türkçe hava durumu açıklamaları
- Sağlık kontrolü endpoint'i

## Kurulum

### 1. Gereksinimler

```bash
pip install -r requirements.txt
```

### 2. API Anahtarı

1. [OpenWeatherMap](https://openweathermap.org/api) sitesinden ücretsiz API anahtarı alın
2. `.env` dosyasını düzenleyin:

```env
OPENWEATHER_API_KEY=your_actual_api_key_here
```

### 3. Servisi Başlatma

```bash
python app.py
```

Servis `http://0.0.0.0:5000` adresinde çalışmaya başlayacak.

## API Kullanımı

### Hava Durumu Sorgulama

**Endpoint:** `GET /weather`

**Parametreler:**
- `city` (zorunlu): Şehir adı

**Örnek İstek:**
```
GET http://localhost:5000/weather?city=Istanbul
```

**Örnek Yanıt:**
```json
{
  "city": "Istanbul",
  "country": "TR",
  "temperature": 22.5,
  "description": "Açık",
  "humidity": 65,
  "wind_speed": 3.2,
  "pressure": 1013,
  "feels_like": 23.1,
  "timestamp": 1699123456
}
```

### Sağlık Kontrolü

**Endpoint:** `GET /health`

**Örnek Yanıt:**
```json
{
  "status": "healthy",
  "service": "Weather MCP Service",
  "version": "1.0.0"
}
```

### Ana Sayfa

**Endpoint:** `GET /`

API kullanım bilgilerini döner.

## Hata Kodları

- `400`: Şehir parametresi eksik
- `401`: API anahtarı geçersiz
- `404`: Şehir bulunamadı
- `408`: İstek zaman aşımı
- `500`: Sunucu hatası
- `503`: Bağlantı hatası

## Test Etme

Farklı şehirler için test:

```bash
curl "http://localhost:5000/weather?city=Istanbul"
curl "http://localhost:5000/weather?city=Ankara"
curl "http://localhost:5000/weather?city=London"
```

## Notlar

- API anahtarınızı `.env` dosyasında saklayın
- Servis varsayılan olarak debug modunda çalışır
- Tüm sıcaklık değerleri Celsius cinsindendir
- Hava durumu açıklamaları Türkçe'dir
