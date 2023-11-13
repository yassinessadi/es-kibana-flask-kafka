import findspark
findspark.init()
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType,BooleanType, IntegerType, ArrayType

SparkSession.builder.config(conf=SparkConf())

spark = SparkSession.builder \
    .appName("KafkaSparkIntegration") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.4,"
            "org.elasticsearch:elasticsearch-spark-30_2.12:8.11.0") \
    .getOrCreate()


df = spark.readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "localhost:9092") \
  .option("subscribe", "jane_essadi") \
  .option("startingOffsets", "earliest") \
  .load()


value_df = df.selectExpr("CAST(value AS STRING)")

# StructType for themoviedb.org

schema = StructType([
    StructField("adult", BooleanType(), True),
    StructField("belongs_to_collection", StructType([
        StructField("name", StringType(), True),
        StructField("poster_path", StringType(), True),
        StructField("backdrop_path", StringType(), True)
    ]), True),
    StructField("budget", IntegerType(), True),
    StructField("genres", ArrayType(StructType([
        StructField("id", IntegerType(), True),
        StructField("name", StringType(), True)
    ])), True),
    StructField("original_language", StringType(), True),
    StructField("overview", StringType(), True),
    StructField("popularity", StringType(), True),
    StructField("production_companies", ArrayType(StructType([
        StructField("id", IntegerType(), True),
        StructField("logo_path", StringType(), True),
        StructField("name", StringType(), True),
        StructField("origin_country", StringType(), True)
    ])), True),
    StructField("production_countries", ArrayType(StructType([
        StructField("iso_3166_1", StringType(), True),
        StructField("name", StringType(), True)
    ])), True),
    StructField("release_date", StringType(), True),
    StructField("revenue", IntegerType(), True),
    StructField("status", StringType(), True),
    StructField("tagline", StringType(), True),
    StructField("title", StringType(), True),
    StructField("video", BooleanType(), True),
    StructField("vote_average", StringType(), True),
    StructField("vote_count", IntegerType(), True)
])


selected_df = value_df.withColumn("values", F.from_json(value_df["value"], schema)).selectExpr("values")

result_df = selected_df.select(
    F.col("values.status").alias("status"),
    F.col("values.overview").alias("overview"),
    F.col("values.production_companies.name").alias("name_production_company"),
    F.col("values.original_language").alias("original_language"),
    F.col("values.tagline").alias("tagline"),
    F.col("values.title").alias("title"),
    F.col("values.video").alias("video"),
    F.col("values.vote_average").alias("vote_average"),
    F.col("values.vote_count").alias("vote_count"),
)


# Write the DataFrame to an Elasticsearch index
# reader = spark.read.format("org.elasticsearch.spark.sql") \
#     .option("es.resource", "index/type") \
#     .option("es.nodes.wan.only", "true") \
#     .option("es.nodes", "localhost") \
#     .option("es.port", "9200") \
#     .option("es.net.ssl", "false") \
#     .option("es.net.http.auth.user", "elastic") \
#     .option("es.net.http.auth.pass", "jane_essadi") \
#     .load()


query = result_df.writeStream \
    .format("org.elasticsearch.spark.sql") \
    .outputMode("append") \
    .option("es.resource", "movies") \
    .option("es.nodes", "localhost") \
    .option("es.port", "9200") \
    .option("es.nodes.wan.only", "true")\
    .option("es.index.auto.create", "true")\
    .option("checkpointLocation", "./checkpointLocation/") \
    .start()

query = result_df.writeStream.outputMode("append").format("console").start()

query.awaitTermination()