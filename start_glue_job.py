import boto3

# Create a Glue client
glue = boto3.client('glue')

# Start the Glue job
response = glue.start_job_run(JobName='spotify-transform-job')

# Print the run ID for tracking
print("Job started with Run ID:", response['JobRunId'])
