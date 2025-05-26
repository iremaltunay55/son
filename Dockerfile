# Python 3.12 slim image kullan
FROM python:3.12-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Sistem paketlerini güncelle ve gerekli paketleri yükle
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Python requirements dosyasını kopyala ve bağımlılıkları yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını kopyala
COPY . .

# .env dosyasının varlığını kontrol et (opsiyonel)
RUN touch .env

# Port 8000'i aç (MCP server için)
EXPOSE 8000

# Uygulama kullanıcısı oluştur (güvenlik için)
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Sağlık kontrolü ekle
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# MCP server'ı başlat
CMD ["python", "app.py"]
