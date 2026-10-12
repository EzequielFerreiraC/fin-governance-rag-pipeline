import os
import pyspark.sql.functions as F
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import StructType, StructField, StringType


def extract_text_content(df: DataFrame) -> DataFrame:
    """Remove unnecessary characters and extract text content from the DataFrame."""
    return df.withColumn(
        "text_content", F.regexp_replace(F.trim(F.col("raw_content")), r"\n+", " ")
    )


def add_audit_columns(df: DataFrame) -> DataFrame:
    """Add audit columns to the DataFrame."""
    return df.withColumn("created_at", F.current_timestamp()).withColumn(
        "layer", F.lit("silver")
    )


def process_bronze_to_silver(
    spark: SparkSession, input_path: str, output_path: str
) -> None:
    """Process the DataFrame from bronze to silver layer by extracting text content and adding audit columns."""

    schema = StructType(
        [
            StructField("id", StringType(), True),
            StructField("raw_content", StringType(), True),
        ]
    )

    if not os.path.exists(input_path):
        print(f"Input path does not exist: {input_path}")
        print("using data tests (mock)")
        data = [
            (
                "BACEN_4893",
                "Art. 1º ...",
            ),
            (
                "CVM_358",
                "    Art. 2º ...",
            ),
        ]
        df_bronze = spark.createDataFrame(data, schema)
    else:
        df_bronze = spark.read.schema(schema).load(input_path)

    df_silver = df_bronze.transform(extract_text_content).transform(add_audit_columns)

    df_silver.select("id", "text_content", "created_at", "layer").show(truncate=False)
    df_silver.select("id", "text_content", "created_at", "layer").write.mode(
    "overwrite"
).parquet(output_path)

    df_silver.write.mode("overwrite").parquet(output_path)
    print(f"Data successfully written in silver layer: {output_path}")


if __name__ == "__main__":
    spark = (
        SparkSession.builder.appName("BronzeToSilver").master("local[*]").getOrCreate()
    )
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    BRONZE_DIR = os.path.join(BASE_DIR, "c_data", "a_raw", "a_bronze")
    SILVER_DIR = os.path.join(BASE_DIR, "c_data", "b_processed", "b_silver")

    process_bronze_to_silver(spark, BRONZE_DIR, SILVER_DIR)
