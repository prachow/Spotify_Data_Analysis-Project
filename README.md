# 🎧 Spotify Data Analysis Project (AWS Data Pipeline)

This project implements a complete data pipeline to analyze Spotify music data using AWS services: S3, Glue, Athena, and QuickSight.

---

## 📌 Pipeline Overview

1. **Upload CSV files** (albums, artists, tracks) to S3 using Python
2. **Catalog datasets** using AWS Glue Crawler
3. **Join datasets** via Glue ETL job (PySpark)
4. **Query with Athena**
5. **Visualize in QuickSight**

---

## 📁 Project Structure
Spotify-Data-Analysis-Project/
├── dataset/                  # Local .csv files
├── scripts/
│   └── join_spotify_data.py  # Glue ETL PySpark script
├── upload_to_s3.py           # Uploads data to S3
├── deploy_glue.py            # Creates Glue DB, Crawler, and Job
├── requirements.txt
└── README.md

---

## ⚙️ Requirements

- Python 3.7+
- AWS CLI (`aws configure`)
- S3 bucket (e.g. `spotifydataa`)
- IAM role with access to S3, Glue, Athena

Install dependencies:
```bash
pip install boto3 tqdm

1. Upload CSVs to S3
        python upload_to_s3.py

2. Deploy Glue Crawler & Job
        python deploy_glue.py

3.Query with Athena
        In the Athena console:
	•	Select database: spotify_db
	•	Query the joined dataset from processed/ location

4. Visualize in QuickSight
	•	Connect to Athena
	•	Select spotify_db > joined_data
	•	Create charts and dashboards

🧠 Built With
	•	AWS S3 – Storage
	•	AWS Glue – Crawler & ETL
	•	AWS Athena – Serverless SQL
	•	AWS QuickSight – Visualization
	•	Python (boto3, tqdm)
