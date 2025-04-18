# Import required libraries
import boto3  # AWS SDK for Python - allows interaction with AWS services like S3
from boto3.s3.transfer import TransferConfig  # Used for configuring large/multipart uploads
from tqdm import tqdm  # For displaying a real-time progress bar
import os  # For file and directory operations

# Define your target S3 bucket name
bucket = 'spotifydataa'

# Define the local folder where your CSV files are located
local_folder = './dataset'

# Define the "folder" prefix inside the S3 bucket where files will be uploaded
prefix = 'raw/'

# Configure how files are uploaded (important for large files)
config = TransferConfig(
    multipart_threshold=8 * 1024 * 1024,   # Files larger than 8MB will be uploaded in parts
    multipart_chunksize=8 * 1024 * 1024,   # Each part will be 8MB
    max_concurrency=5,                     # Up to 5 parts can upload in parallel
    use_threads=True                       # Enable multithreading for concurrency
)

# Create an S3 client using your AWS credentials from `aws configure`
s3 = boto3.client('s3')

# Function to upload a single file to S3 with a progress bar
def upload_with_progress(filename, key):
    # Build full path to the local file
    file_path = os.path.join(local_folder, filename)

    # Get the size of the file (used to set progress bar range)
    filesize = os.path.getsize(file_path)

    # Create a tqdm progress bar with total size in bytes
    progress = tqdm(
        total=filesize,
        unit='B',           # Unit: bytes
        unit_scale=True,    # Scale automatically to KB/MB/GB
        desc=f"Uploading {filename}"  # Label next to progress bar
    )

    # Define a callback function that updates the progress bar
    def callback(bytes_transferred):
        progress.update(bytes_transferred)  # Called every time part of the file is uploaded

    try:
        # Start uploading the file using multipart upload
        s3.upload_file(
            Filename=file_path,    # Local file path
            Bucket=bucket,         # Target S3 bucket
            Key=key,               # Full S3 path ("raw/filename.csv")
            Config=config,         # Use TransferConfig for multipart support
            Callback=callback      # Update progress bar on each upload chunk
        )
        progress.close()           # Close the progress bar once done
        print(f"Finished: {filename}")  # Print success message
    except Exception as e:
        progress.close()           # Close the progress bar if there's an error
        print(f"Failed: {e}")      # Print error message

# Loop through all files in the dataset folder
for file in os.listdir(local_folder):
    # Process only .csv files
    if file.endswith('.csv'):
        # Create the destination path in S3 (e.g., 'raw/albums.csv')
        s3_key = prefix + file

        # Call the function to upload the file with progress tracking
        upload_with_progress(file, s3_key)