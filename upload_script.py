import boto3

s3 = boto3.client('s3')

# Replace with your actual bucket name and path
bucket_name = 'spotifydataa'  
script_path_in_s3 = 'scripts/spotify_transform.py'

# Upload local script to S3
s3.upload_file('spotify_transform.py', bucket_name, script_path_in_s3)

print("Script uploaded successfully to S3!")
