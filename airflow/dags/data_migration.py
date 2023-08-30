import argparse
from pathlib import Path
from sqlalchemy import text
from model import Connection
import config

# Initialize Table
def main(db_connection):
    Path(config.CSV_DIR).mkdir(parents=True, exist_ok=True)
    
    connection = Connection(db_connection)
    session = connection.get_session()

    sql_statement = text('''
        CREATE TABLE IF NOT EXISTS traffic_report (
            timestamp BIGINT PRIMARY KEY,
            traffic_report_id VARCHAR(255), 
            date_time TIMESTAMP, 
            issue_reported VARCHAR(255),
            latitude DECIMAL, 
            longitude DECIMAL, 
            address VARCHAR(255),
            weekday VARCHAR(50),
            date DATE,
            time TIME)
    ''')
    
    session.execute(sql_statement)
    session.commit()
    session.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--connection", required=True, type=str)
    args = parser.parse_args()
    main(args.connection)