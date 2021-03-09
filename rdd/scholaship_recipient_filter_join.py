from pyspark.sql import SparkSession, Row
from distutils.util import strtobool
import os.path
import yaml
import sys

if __name__ == '__main__':

    os.environ["PYSPARK_SUBMIT_ARGS"] = (
        '--packages "org.apache.hadoop:hadoop-aws:2.7.4" pyspark-shell'
    )

    # Create the SparkSession
    spark = SparkSession \
        .builder \
        .appName("RDD examples") \
        .master('local[*]') \
        .getOrCreate()
    spark.sparkContext.setLogLevel('ERROR')

    current_dir = os.path.abspath(os.path.dirname(__file__))
    app_config_path = os.path.abspath(current_dir + "/../" + "application.yml")
    app_secrets_path = os.path.abspath(current_dir + "/../" + ".secrets")

    conf = open(app_config_path)
    app_conf = yaml.load(conf, Loader=yaml.FullLoader)
    secret = open(app_secrets_path)
    app_secret = yaml.load(secret, Loader=yaml.FullLoader)

    # Setup spark to use s3
    hadoop_conf = spark.sparkContext._jsc.hadoopConfiguration()
    hadoop_conf.set("fs.s3a.access.key", app_secret["s3_conf"]["access_key"])
    hadoop_conf.set("fs.s3a.secret.key", app_secret["s3_conf"]["secret_access_key"])

    coursesRDD = spark.sparkContext.textFile("s3a://" + app_conf["s3_conf"]["s3_bucket"] + "/course.csv")
    coursesRDD.toDF().show();

    #coursesRDD \
     #   .toDF() \
      #  .write \
       # .mode("overwrite") \
        #.option("delimiter", "~") \
        #.csv("s3a://" + app_conf["s3_conf"]["s3_bucket"] + "/result")

# spark-submit --packages "org.apache.hadoop:hadoop-aws:2.7.4" rdd/scholaship_recipient_filter_join.py
