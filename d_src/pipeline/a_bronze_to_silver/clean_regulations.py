from pathlib import Path

import pyspark.sql.functions as F
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import StructField, StringType, StructType


def get_project_data_paths() -> tuple[Path, Path]:
    """Return bronze and silver data paths from the project root."""
    project_root = Path(__file__).resolve().parents[3]
    if not (project_root / "README.md").exists():
        project_root = Path(__file__).resolve().parents[2]

    return (
        project_root / "c_data" / "a_raw" / "a_bronze",
        project_root / "c_data" / "b_processed" / "b_silver",
    )


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
    spark: SparkSession, input_path: str | Path, output_path: str | Path
) -> None:
    """Process the DataFrame from bronze to silver layer by extracting text content and adding audit columns."""
    input_path = Path(input_path)
    output_path = Path(output_path)

    schema = StructType(
        [
            StructField("id", StringType(), True),
            StructField("raw_content", StringType(), True),
        ]
    )

    if not input_path.exists():
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
        df_bronze = spark.read.schema(schema).load(str(input_path))

    df_silver = df_bronze.transform(extract_text_content).transform(add_audit_columns)
    silver_df = df_silver.select("id", "text_content", "created_at", "layer")

    silver_df.show(truncate=False)
    silver_df.write.mode("overwrite").parquet(str(output_path))
    print(f"Data successfully written in silver layer: {output_path}")


if __name__ == "__main__":
    spark = (
        SparkSession.builder.appName("BronzeToSilver").master("local[*]").getOrCreate()
    )
    BRONZE_DIR, SILVER_DIR = get_project_data_paths()

    process_bronze_to_silver(spark, BRONZE_DIR, SILVER_DIR)
