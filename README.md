# Hava Durumu MCP Server

OpenWeather API kullanarak hava durumu bilgilerini sağlayan MCP (Model Context Protocol) server.

## Özellikler

- ✅ **MCP Protocol** - Model Context Protocol desteği
- 🌤️ **OpenWeather API** - Gerçek zamanlı hava durumu verileri
- 🛠️ **MCP Tools** - `get_weather` aracı ile şehir bazlı sorgulama
- 🔒 **Güvenli** - Environment variable ile API anahtarı yönetimi
- 🐳 **Docker** - Containerized deployment
- 📡 **Smithery** - Smithery.ai platformu ile kolay deploy

## MCP Nedir?

Model Context Protocol (MCP), AI modellerinin dış araçlara ve kaynaklara güvenli bir şekilde erişmesini sağlayan açık protokoldür.

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

### 3. MCP Server'ı Başlatma

```bash
python app.py
```

Server MCP protokolü ile stdin/stdout üzerinden iletişim kuracak.

## MCP Tools

### get_weather

Belirtilen şehir için güncel hava durumu bilgilerini alır.

**Parametreler:**
- `city` (string, zorunlu): Şehir adı (örn: Istanbul, Ankara, London)

**Örnek Kullanım:**
```json
{
  "name": "get_weather",
  "arguments": {
    "city": "Istanbul"
  }
}
```

**Örnek Yanıt:**
```
🌤️ İstanbul, TR Hava Durumu:

🌡️ Sıcaklık: 22.5°C (Hissedilen: 23.1°C)
☁️ Durum: Açık
💧 Nem: 65%
🌬️ Rüzgar: 3.2 m/s
📊 Basınç: 1013 hPa

📅 Güncelleme: 1699123456
```

## Smithery Deployment

### 1. Repository'yi Smithery'e Push Edin

```bash
git add .
git commit -m "MCP server ready for deployment"
git push origin main
```

### 2. Smithery.ai'da Deploy Edin

1. [Smithery.ai](https://smithery.ai) hesabınıza giriş yapın
2. Repository'nizi bağlayın
3. `smithery.yaml` otomatik olarak algılanacak
4. Deploy butonuna tıklayın

### 3. Environment Variables

Smithery dashboard'da şu environment variable'ı ayarlayın:
- `OPENWEATHER_API_KEY`: OpenWeather API anahtarınız

## Docker ile Çalıştırma

```bash
# Image'ı build et
docker build -t weather-mcp-server .

# Container'ı çalıştır
docker run -e OPENWEATHER_API_KEY=your_api_key weather-mcp-server
```

## MCP Client Entegrasyonu

Bu server'ı MCP destekleyen herhangi bir AI client ile kullanabilirsiniz:

- **Claude Desktop**
- **VS Code MCP Extension**
- **Custom MCP Clients**

## Notlar

- ✅ MCP Protocol 2024-11-05 uyumlu
- ✅ Async/await desteği
- ✅ Proper error handling
- ✅ Docker containerized
- ✅ Smithery.ai ready
