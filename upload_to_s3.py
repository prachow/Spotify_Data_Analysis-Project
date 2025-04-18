import boto3 # type: ignore

# Replace with your actual AWS credentials
aws_access_key = "*******************"
aws_secret_key = "*************************************************************"
region_name = "us-east-1"  # or your desired region

# Create S3 client with credentials
s3 = boto3.client(
    's3',
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=region_name
)

# Config
bucket_name = 'spotifydataa'
file_path = './spotify-2023.csv'
s3_key = 'spotify-data/spotify-2023.csv'

# Upload
try:
    s3.upload_file(file_path, bucket_name, s3_key)
    print(f"Upload successful! File available at: s3://{bucket_name}/{s3_key}")
except Exception as e:
    print(f"Upload failed: {e}")
