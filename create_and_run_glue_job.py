import boto3

glue = boto3.client('glue')

try:
    response = glue.create_job(
        Name='spotify-transform-job',
        Role='arn:aws:iam::857220980520:user/spotify_user',  # Make sure this role has all required permissions
        ExecutionProperty={'MaxConcurrentRuns': 1},
        Command={
            'Name': 'glueetl',
            'ScriptLocation': 's3://spotifydataa/scripts/spotify_transform.py',
            'PythonVersion': '3'
        },
        MaxRetries=0,
        GlueVersion='3.0',
        Timeout=30
    )
    print("Glue job created.")
except glue.exceptions.AlreadyExistsException:
    print("Job already exists. Skipping creation.")

# Start the Glue job
job_run = glue.start_job_run(JobName='spotify-transform-job')
print("Job started with Run ID:", job_run['JobRunId'])
