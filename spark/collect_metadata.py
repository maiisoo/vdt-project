import json

from pyspark.sql import SparkSession

if __name__ == '__main__':
    spark = SparkSession.builder \
        .appName("GetMetadata") \
        .enableHiveSupport() \
        .getOrCreate()

    tables = spark.sql("SHOW TABLES").collect()

    metadata_dict = {}

    for table in tables:
        table_name = table['tableName']
        metadata_dict[table_name] = {}

        schema_df = spark.sql(f"DESCRIBE {table_name}")
        schema_list = schema_df.collect()
        metadata_dict[table_name]['schema'] = [
            {'column': row['col_name'], 'type': row['data_type'], 'comment': row['comment']} for row in schema_list]

    output_file_path = "metadata/metadata.jsonl"
    with open(output_file_path, "w") as f:
        json.dump(metadata_dict, f, indent=4)

    spark.stop()