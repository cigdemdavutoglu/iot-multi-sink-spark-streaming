# IoT Telemetry Streaming with Spark Structured Streaming

Bu proje, IoT cihazlarından gelen sensör verilerini gerçek zamanlı olarak okuyup, belirli kurallara göre **üç farklı hedefe** yazan bir **Spark Structured Streaming** uygulamasıdır.

## 📌 Projenin Amacı

Gerçek zamanlı veri işleme ile:
- `device` ID'sine göre verileri filtrelemek,
- Filtrelenen verileri farklı hedeflere yönlendirmek:
  - 🔁 **PostgreSQL** (device: `00:0f:00:70:91:0a`)
  - 🐝 **Hive (Parquet)** (device: `b8:27:eb:bf:9d:51`)
  - 🌀 **Delta Lake (HDFS)** (device: `1c:bf:ce:15:ec:4d`)
 
  ## 📂 Veri ve Tablo Oluşturma

 **ÖNEMLİ:** Bu proje için Spark ve Hadoop ortamınızın doğru şekilde kurulmuş ve yapılandırılmış olması gerekmektedir.

-Kullanılan IoT sensör verileri `iot_telemetry_data.csv.zip` dosyasında bulunur.

-Sanal makinenin terminalinde output dosyası oluşturulur ve bu dosyanın bulunduğu klasörün dizimine gelindikten sonra venvspark (source venvspark/bin/activate) aktif edildilir.

-python dataframe_to_log.py -i ~/datasets/iot_telemetry_data.csv -idx True (Bu komut, verileri output klasörüne yazıp streamin veri almasını sağlar.) komutuyla çalıştırılır.

--Sink oluşturma:
- Hive tablosu, DBeaver kullanılarak manuel oluşturulabilir.
-   CREATE TABLE test1.sensor_51 (
    row_id INT,
    event_ts DOUBLE,
    device STRING,
    co FLOAT,
    humidity FLOAT,
    light BOOLEAN,
    lpg FLOAT,
    motion BOOLEAN,
    smoke FLOAT,
    temp FLOAT,
    generate_ts TIMESTAMP
)
STORED AS PARQUET;
  Tablo yapısı ve adı: `test1.sensor_51`  
  (Gerekirse Hive terminal veya DBeaver üzerinden oluşturulabilir.)

- PostgreSQL tablosu streaming sırasında otomatik oluşturulmaktadır.

- Delta tablosu, `create_delta_table.py` dosyası ile HDFS üzerinde oluşturulmuştur.

- read_from_csv.py dosyası çalıştırılır.(Bu dosya veriyi gerçek zamanlı olarak okur,veriyi device ID’sine göre filtreler,filtrelenen verileri üç farklı hedefe (PostgreSQL, Hive, Delta Lake) yazmak için kullanılır.)
- İlgili verilerin sink'lerdeki tablolara gidip gitmediğini görmek için sorgulama yapılır.
- Delta table için read_delta_table.py dosyası çalıştırılarak gelen veriler gözlenlenir.
- Postgresql ve hive için dbeaver'da bağlantı sağlanıp select sorgusu atılarak gözlemlenebilir.


## 🧱 Proje Yapısı

- `read_from_csv.py`       : Spark Structured Streaming uygulaması,
- `create_delta_table.py`  : Delta tablosunu HDFS üzerinde oluşturan script,
- `read_delta_table.py`    : Delta tablosundaki verileri okuyan script,
- `iot_telemetry_data.csv.zip` : IoT sensör veri seti,
- `requirements.txt`       : Projede kullanılan Python paketleri,
- `README.md`              : Proje açıklaması ve kullanım rehberi,
- `LICENSE`                : Proje lisansı,
- `.gitignore`             : Git tarafından yok sayılacak dosya/klasörler.


## ⚙️ Kullanım

1. Projeyi klonlayın veya indirin:
```bash
git clone <repo-url>
cd <repo-folder>

## ⚙️ Gerekli Python paketlerini yükleyin
pip install -r requirements.txt
spark-submit read_from_csv.py



