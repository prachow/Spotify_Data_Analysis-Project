import sys
from pyspark.context import SparkContext # type: ignore
from awsglue.context import GlueContext # type: ignore
from awsglue.utils import getResolvedOptions # type: ignore
from awsglue.job import Job # type: ignore

args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Load from catalog (assuming crawler already ran)
dyf = glueContext.create_dynamic_frame.from_catalog(
    database="spotify_raw_db",
    table_name="spotify_raw_table"
)

# Transform: drop duplicates
df = dyf.toDF().dropDuplicates()

# Convert back to DynamicFrame
dyf_transformed = glueContext.create_dynamic_frame.from_df(df, glueContext, "dyf_transformed")

# Write to S3 as Parquet (Athena-friendly)
glueContext.write_dynamic_frame.from_options(
    frame=dyf_transformed,
    connection_type="s3",
    connection_options={"path": "s3://spotify-data-transformed/processed/"},
    format="parquet"
)

job.commit()
