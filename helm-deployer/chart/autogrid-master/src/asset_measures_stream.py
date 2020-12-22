import json
import os
import datetime
import configparser
import time

from pyspark.sql import SparkSession, functions as F
from pyspark.sql.functions import *

SECRETS_PATH = '/etc/secrets/'

APP_CONF = {}

def load_conf(SECRETS_PATH):
    with os.scandir(SECRETS_PATH) as entries:
        for entry in entries:
            key: str = entry.name
            print("key is : ", key)
            if key.startswith('.'):
              continue
            f=open(os.path.join(SECRETS_PATH,entry),'r')
            value: str=f.readline().strip()
            APP_CONF[key] = value
            # print("value is : ", value)
  
#  persist_batch function to persist dataframe
def persist_batch(df, epochId):
  print("Process Batch ", epochId)
  print("Total records in batch :", df.count())
  df = df.coalesce(1)
  df.cache()
  df.show(5, False)
  if (APP_CONF["spark.persist"] == 's3' or APP_CONF["spark.persist"] == "s3db"):
    persist_s3(df, epochId)
  if (APP_CONF["spark.persist"] == 'db' or APP_CONF["spark.persist"] == "s3db"):
    persist_tsdb(df, epochId)
  df.unpersist()
  
def persist_tsdb(df, epochId):
  #persist to timescaledb
  df.write \
  .format("jdbc") \
  .mode("append") \
  .option("url", APP_CONF["tsdb.url"]) \
  .option("dbtable", APP_CONF["tsdb.table"]) \
  .option("user", APP_CONF["tsdb.user"]) \
  .option("password", APP_CONF["tsdb.password"]) \
  .save()

def persist_s3(df, epochId):

  #add year, month, day columns for s3 partition
  df = df.withColumn("year", year("date"))
  df = df.withColumn('month', month("date"))
  df = df.withColumn('day', dayofmonth("date"))


  #persist to s3
  df.write \
    .format("parquet") \
    .mode("append") \
    .option("path", APP_CONF['aws.path']) \
    .option("truncate","false") \
    .partitionBy("year", "month", "day") \
    .option("fs.s3a.committer.name", "partitioned") \
    .option("fs.s3a.committer.staging.conflict-mode", "append") \
    .save()
    # .option("spark.sql.sources.commitProtocolClass", "org.apache.spark.internal.io.cloud.PathOutputCommitProtocol") \
    # .option("spark.sql.parquet.output.committer.class", "org.apache.spark.internal.io.cloud.BindingParquetOutputCommitter") \

load_conf('/etc/secrets/')
print("Starting sleep for debug")
time.sleep(60)
print("Stoping sleep")
spark = SparkSession.builder.appName("AutoGrid-Kafka-Consume-Persist").master(APP_CONF["spark.master"]).getOrCreate()
spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.access.key", APP_CONF["aws.accesskey"])
spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.secret.key", APP_CONF["aws.secretkey"])
spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.assumed.role.arn", APP_CONF["aws.role"])
spark.sparkContext._jsc.hadoopConfiguration().set("mapreduce.outputcommitter.factory.scheme.s3a", "org.apache.hadoop.fs.s3a.commit.S3ACommitterFactory")
spark.sparkContext._jsc.hadoopConfiguration().set("mapreduce.fileoutputcommitter.algorithm.version", "1")
spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.committer.name", "partitioned")
spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.committer.staging.conflict-mode", "append")
spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.buffer.dir", "s3-stage")
  
df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", APP_CONF["kafka.server"]) \
  .option("startingOffsets", APP_CONF["spark.startingoffsets"]) \
  .option("failOnDataLoss", "false") \
  .option("subscribe", APP_CONF["kafka.topic"]) \
  .option("kafka.security.protocol" , "SSL") \
  .option("kafka.ssl.keystore.location" , "/var/private/ssl/kafka.client.keystore.jks") \
  .option("kafka.ssl.keystore.password", APP_CONF["keystore.password"]) \
  .option("kafka.ssl.truststore.location", "/usr/local/openjdk-8/jre/lib/security/cacerts") \
    .load() \
  .selectExpr("CAST(value AS STRING)")
df.printSchema()
  
  # .option("failOnDataLoss", "false") \

autogridSchema = spark.read.json(APP_CONF["message.schema"]).schema

#Kafka message is key, value pair. get the value string and parse as json
jsonDF =  df.select(from_json("value",autogridSchema).alias("values"))
jsonDF.printSchema()

#Explode json to flatten json structure
explodedDF1 = jsonDF.select(F.col("values.message_id").alias("message_id"), F.col("values.timestamp_utc").alias("message_timestamp_utc"), F.col("values.tenant_uid").alias("tenant_uid"), F.col("values.source").alias("source"), F.col("values.stream_type").alias("stream_type"), F.explode("values.payload").alias("payload"))
explodedDF1.printSchema()

#Format columns to proper type
destDF1 = explodedDF1.select("message_id", to_timestamp(col("message_timestamp_utc")).alias("message_timestamp_utc"), "tenant_uid", "source", "stream_type", "payload.identifier", "payload.value", to_timestamp(col("payload.timestamp_utc")).alias("timestamp_utc"), to_date(col("payload.timestamp_utc")).alias("date"))

#gather records for the batch duration and call persist_batch to persist  
destDF1.writeStream.trigger(processingTime=APP_CONF["spark.batchtime"]).foreachBatch(persist_batch).option("checkpointLocation", APP_CONF["spark.checkpoint"]).start().awaitTermination()
