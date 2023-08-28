import argparse
import os
import csv
from datetime import timedelta, datetime

from model import Connection, Traffic
import config

def get_yesterday_date(fetch_date):
    return datetime.strptime(fetch_date, '%Y-%m-%d').date() - timedelta(1)

def get_file_path(fetch_date):
    yesterday = get_yesterday_date(fetch_date)
    filename = "traffic_{}.csv".format(yesterday)
    return os.path.join(config.CSV_DIR, filename)

def main(fetch_date, db_connection):
    yesterday = get_yesterday_date(fetch_date)
    filename = get_file_path(fetch_date)
    data_insert = []
    
    with open(filename, encoding='utf-8') as csvf:
        csv_reader = csv.DictReader(csvf)
        for row in csv_reader:
            traffic_data = Traffic(timestamp=row['timestamp'],
                                traffic_report_id=row['traffic_report_id'],
                                date_time=row['date_time'],
                                issue_reported=row['issue_reported'],
                                location=row['location'],
                                latitude=row['latitude'],
                                longitude=row['longitude'],
                                address=row['address'],
                                weekday=row['weekday'],
                                date=row['date'],
                                time=row['time'])
            data_insert.append(traffic_data)

    connection = Connection(db_connection)
    session = connection.get_session()
    session.execute("DELETE FROM traffic_report where date_time >= timestamp '{} 00:00:00' and date_time < timestamp'{} 00:00:00'".format(yesterday, fetch_date))
    session.bulk_save_objects(data_insert)
    session.commit()
    session.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True, type=str)
    parser.add_argument("--connection", required=True, type=str)
    args = parser.parse_args()
    main(args.date, args.connection)