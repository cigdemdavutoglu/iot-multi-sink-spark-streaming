# IoT Telemetry Streaming with Spark Structured Streaming

Bu proje, IoT cihazlarından gelen sensör verilerini gerçek zamanlı olarak okuyup, belirli kurallara göre **üç farklı hedefe** yazan bir **Spark Structured Streaming** uygulamasıdır.

## 📌 Projenin Amacı

Gerçek zamanlı veri işleme ile:
- `device` ID'sine göre verileri filtrelemek,
- Filtrelenen verileri farklı hedeflere yönlendirmek:
  - 🔁 **PostgreSQL** (device: `00:0f:00:70:91:0a`)
  - 🐝 **Hive (Parquet)** (device: `b8:27:eb:bf:9d:51`)
  - 🌀 **Delta Lake (HDFS)** (device: `1c:bf:ce:15:ec:4d`)

## 🧱 Proje Yapısı

- `read_from_csv.py`: Spark Structured Streaming uygulaması,
- `conf/`: Hive ve Spark konfigürasyon dosyaları,
- `data-generator/output/`: Gelen CSV veri dosyaları,
- `checkpoint/`: Streaming checkpoint klasörü,
- `requirements.txt`: Gerekli Python paketleri (varsa).

## ⚙️ Kullanım

1. Projeyi klonlayın veya indirin:
```bash
git clone <repo-url>
cd <repo-folder>

## Gerekli Python paketlerini yükleyin:
pip install -r requirements.txt
spark-submit read_from_csv.py



