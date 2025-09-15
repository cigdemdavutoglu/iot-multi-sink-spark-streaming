# Gerekli Spark ve veri türü sınıflarını içe aktar
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, DoubleType, StringType, FloatType, BooleanType, TimestampType

# Spark oturumu oluştur (Delta Lake desteği ile)
spark = SparkSession.builder \
    .appName("Create Delta Table") \
    .master("local[2]") \
    .config("spark.jars.packages", "io.delta:delta-core_2.12:0.7.0") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

# Delta tablosu için kullanılacak şema tanımlanıyor
schema = StructType([
    StructField("row_id", IntegerType()),
    StructField("event_ts", DoubleType()),
    StructField("device", StringType()),
    StructField("co", FloatType()),
    StructField("humidity", FloatType()),
    StructField("light", BooleanType()),
    StructField("lpg", FloatType()),
    StructField("motion", BooleanType()),
    StructField("smoke", FloatType()),
    StructField("temp", FloatType()),
    StructField("generate_ts", TimestampType()),
])

# Yukarıdaki şemayı kullanarak boş bir DataFrame oluştur
empty_df = spark.createDataFrame([], schema)

# Delta tablosunu HDFS üzerinde belirtilen konuma kaydet
delta_path = "hdfs://localhost:9000/user/train/deltaPathSensor4d"
empty_df.write.format("delta").mode("overwrite").save(delta_path)

print("Delta tablosu başarıyla oluşturuldu.")
