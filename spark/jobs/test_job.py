from pyspark.sql import SparkSession
from pyspark.sql import functions as F


def main():
    spark = SparkSession.builder.appName("test_job").getOrCreate()

    df = spark.range(1, 1_000_001)
    result = df.agg(
        F.count("id").alias("row_count"),
        F.sum("id").alias("total"),
    )
    result.show()

    spark.stop()


if __name__ == "__main__":
    main()