import boto3
import time

# Setup
athena_client = boto3.client('athena', region_name='us-east-1')  # change region if needed
DATABASE = 'spotify_db'
OUTPUT_LOCATION = 's3://spotifyresultsql/'  # change to your S3 bucket

def run_athena_query(query, description="Query"):
    print(f"\nRunning: {description}")
    response = athena_client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={'Database': DATABASE},
        ResultConfiguration={'OutputLocation': OUTPUT_LOCATION}
    )
    query_execution_id = response['QueryExecutionId']

    # Wait for completion
    while True:
        status = athena_client.get_query_execution(QueryExecutionId=query_execution_id)['QueryExecution']['Status']['State']
        if status in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
            break
        time.sleep(2)

    if status == 'SUCCEEDED':
        print(f"{description} succeeded: QueryExecutionId = {query_execution_id}")
    else:
        print(f"{description} failed with status: {status}")

# --------------------------
# Query 1: Top 10 streamed songs
query1 = """
SELECT 
  track_name, 
  "artist(s)_name", 
  CAST(streams AS BIGINT) AS total_streams
FROM spotify_spotify_data
WHERE try(CAST(streams AS BIGINT)) IS NOT NULL
ORDER BY total_streams DESC
LIMIT 10;
"""
run_athena_query(query1, "Top 10 Most Streamed Songs")

# --------------------------
# Query 2: Most streamed artist per year
query2 = """
WITH ranked_artists AS (
    SELECT 
        released_year,
        "artist(s)_name",
        SUM(CAST(streams AS BIGINT)) AS total_streams,
        ROW_NUMBER() OVER (PARTITION BY released_year ORDER BY SUM(CAST(streams AS BIGINT)) DESC) AS rank
    FROM spotify_spotify_data
    WHERE try(CAST(streams AS BIGINT)) IS NOT NULL
    GROUP BY released_year, "artist(s)_name"
)
SELECT released_year, "artist(s)_name", total_streams
FROM ranked_artists
WHERE rank = 1;
"""
run_athena_query(query2, "Most Streamed Artist Per Year")

# --------------------------
# Query 3: Average danceability, valence, energy per year
query3 = """
SELECT 
    released_year,
    AVG("danceability_%") AS avg_danceability,
    AVG("valence_%") AS avg_valence,
    AVG("energy_%") AS avg_energy
FROM spotify_spotify_data
GROUP BY released_year
ORDER BY released_year;
"""
run_athena_query(query3, "Avg Danceability, Valence, Energy per Year")
