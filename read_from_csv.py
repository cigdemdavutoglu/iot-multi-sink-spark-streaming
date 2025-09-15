# findspark ile Spark kurulum yolunu belirtip Spark'ı başlatıyoruz
import findspark
findspark.init("/opt/manual/spark")
from pyspark.sql import SparkSession, functions as F

# SparkSession oluşturuluyor, yapılandırma ayarları yapılıyor
spark = SparkSession.builder \
    .master("local[2]") \
    .appName("Device Foreach Multiple Sinks") \
    .config("spark.executor.memory", "3g") \
    .config("spark.driver.memory", "1g") \
    .config("spark.jars.packages", "io.delta:delta-core_2.12:0.7.0") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .enableHiveSupport() \
    .getOrCreate()

# Log seviyesini ERROR olarak ayarlıyoruz, böylece sadece hata mesajları gösterilir
spark.sparkContext.setLogLevel('ERROR')

# Veri şeması: IoT sensör verilerinin kolon ve tipleri
iot_schema = "row_id int, event_ts double, device string, co float, humidity float, light boolean, " \
             "lpg float, motion boolean, smoke float, temp float, generate_ts timestamp"

# PostgreSQL bağlantı bilgileri
jdbcUrl = "jdbc:postgresql://localhost/traindb?user=train&password=Ankara06"
# Delta Lake verisinin kaydedileceği HDFS yolu
deltaPathSensor4d = "hdfs://localhost:9000/user/train/deltaPathSensor4d"


# Streaming veri kaynağı olarak CSV dosyalarını okuyoruz
lines = (spark.readStream
         .format("csv")
         .schema(iot_schema)
         .option("header", False)
         .option("maxFilesPerTrigger", 1)
         .load("file:///home/train/data-generator/output"))

import os
import shutil
import glob


# Streaming batch başına çalışan fonksiyon, burada veriler filtrelenip farklı hedeflere yazılıyor
def write_to_multiple_sinks(df, batchId):
    df.persist()       # DataFrame belleğe alınıyor performans için
    print(f"Batch {batchId} data:")
    df.show()         # Gelen batch verisi konsola yazdırılıyor

    # Filtrelenmiş örnek gösterimler, debug amaçlı
    df.filter("device = '00:0f:00:70:91:0a'").show()
    df.filter("device = 'b8:27:eb:bf:9d:51'").show()
    df.filter("device = '1c:bf:ce:15:ec:4d'").show()

    # PostgreSQL'e yazma (cihaz ID'si 00:0f:00:70:91:0a olanlar)
    df.filter("device = '00:0f:00:70:91:0a'") \
        .write.jdbc(url=jdbcUrl,
                    table="sensor_0a",
                    mode="append",
                    properties={"driver": 'org.postgresql.Driver'})

    # Hive (Parquet formatında) yazma (cihaz ID'si b8:27:eb:bf:9d:51 olanlar)
    df.filter("device = 'b8:27:eb:bf:9d:51'") \
        .write.format("parquet") \
        .mode("append") \
        .insertInto("test1.sensor_51")

    # Delta Lake (HDFS üzerinde) yazma (cihaz ID'si 1c:bf:ce:15:ec:4d olanlar)
    df.filter("device = '1c:bf:ce:15:ec:4d'") \
        .write.format("delta") \
        .mode("append") \
        .save(deltaPathSensor4d)

    df.unpersist()      # Bellekte tutulan veriyi serbest bırakıyoruz


# Checkpoint klasörünün yolu
checkpointDir = "file:///home/train/checkpoint/iot_multiple_sink_foreach_batch"

# Streaming sorgusunu başlatıyoruz
streamingQuery = (lines
                  .writeStream
                  .foreachBatch(write_to_multiple_sinks)
                  .option("checkpointLocation", checkpointDir)
                  .start())

# Streaming sorgusunun sürekli çalışmasını sağlıyor
streamingQuery.awaitTermination()
