import psycopg2
import json

def check_cron_jobs_status():
    # Database connection parameters
    db_params = {
        'database': 'dummydb',
        'user': 'jenkins_user',
        'password': 'dummyDB',
        'host': '172.28.144.49',
        'port': '5432'
    }

    # Connect to the database
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()

    # Query to select job_name and is_online from the cron_jobs table
    query = "SELECT job_name, is_online FROM cron_jobs"

    # Create a list to store the names of offline jobs
    offline_jobs = []

    try:
        cursor.execute(query)
        records = cursor.fetchall()

        for record in records:
            job_name, is_online = record
            if not is_online:
                offline_jobs.append(job_name)  # Add the offline job name to the list

        # Return the list of offline jobs as a JSON string
        return json.dumps(offline_jobs)

    except Exception as e:
        return json.dumps({"error": str(e)})
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    offline_jobs = check_cron_jobs_status()
    print(offline_jobs)