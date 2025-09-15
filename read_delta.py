# findspark, Spark'ı Python ortamına tanıtmak için kullanılır
import findspark

# Spark'ın kurulu olduğu dizini belirt
findspark.init("/opt/manual/spark")

# Gerekli PySpark sınıflarını içe aktar
from pyspark.sql import SparkSession, functions as F

# Spark oturumu oluşturuluyor
spark = SparkSession.builder \
    .master("local[2]") \
    .appName("Read delta table") \
    .config("spark.executor.memory", "3g") \
    .config("spark.driver.memory", "1g") \
    .config("spark.jars.packages", "io.delta:delta-core_2.12:0.7.0") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .enableHiveSupport() \
    .getOrCreate()

# Spark loglarını sadeleştirmek için sadece ERROR seviyesini göster
spark.sparkContext.setLogLevel("ERROR")

# Delta tablosunun HDFS üzerindeki yolu
deltaPathSensor4d = "hdfs://localhost:9000/user/train/deltaPathSensor4d"

# Delta formatındaki verileri okuyarak bir DataFrame oluştur
delta_table = spark.read.format("delta").load(deltaPathSensor4d)

# Toplam satır sayısını yazdır
print("row count ", delta_table.count())

# Delta tablosunun verilerini terminale yazdır
delta_table.show()

