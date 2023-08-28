import requests, argparse, os
import pandas as pd
import json
from datetime import timedelta, datetime

import config

rename_header = { 'Traffic Report ID'  : 'traffic_report_id', 
                  'Published Date'     : 'date_time', 
                  'Issue Reported'     : 'issue_reported', 
                  'Location'           : 'location', 
                  'Latitude'           : 'latitude', 
                  'Longitude'          : 'longitude',
                  'Address'            : 'address',
                  'Status'             : 'status',
                  'Status Date'        : 'status_date'}

reposition_header = ['timestamp', 'traffic_report_id', 'date_time', 'issue_reported', 'location', 'latitude', 'longitude', 'address',
                     'status', 'status_date']

def get_yesterday_date(get_date):
    return datetime.strptime(get_date, '%Y-%m-%d').date() - timedelta(1)

def get_file_path(get_date):
    yesterday = get_yesterday_date(get_date)
    filename = "dailytraffic_{}.csv".format(yesterday)
    return os.path.join(config.CSV_DIR, filename)

def import_data():
    url = config.TRAFFIC_API
    data_req = requests.get(url)
    data_json = data_req.json()
    return data_json

# Fill missing location values with combined latitude and longitude
def combine_lat_lon(row):
    if pd.isna(row['location']) and not (pd.isna(row['latitude']) or pd.isna(row['longitude'])):
        return f"({row['latitude']}, {row['longitude']})"
    else:
        return row['location']

def transform_data(data_json):
    dataframe = pd.DataFrame(data_json['data'])
    df = dataframe.rename(columns = rename_header)
    df['timestamp'] = df['date_time'].copy()
    df = df[reposition_header]

    # clean-up data

    # Cleaning String
    df.loc[:, 'issue_reported'] = df['issue_reported'].str.lower()
    df.loc[:, 'address'] = df['address'].str.lower()
    df.loc[:, 'issue_reported'] = df['issue_reported'].str.strip()
    df.loc[:, 'issue_reported'] = df['issue_reported'].str.replace(r'\s+', ' ', regex=True)
    df.loc[:, 'address'] = df['address'].str.strip()
    df.loc[:, 'address'] = df['address'].str.replace(r'\s+', ' ', regex=True)

    # Cleaning Issues
    df.loc[df['issue_reported'] == 'trfc hazd/ debris', 'issue_reported'] = 'traffic hazard'
    df.loc[df['issue_reported'] == 'zstalled vehicle', 'issue_reported'] = 'stalled vehicle'
    df.loc[df['issue_reported'] == 'n / hzrd trfc viol', 'issue_reported'] = 'traffic hazard'
    df.loc[df['issue_reported'] == 'collisn / ftsra', 'issue_reported'] = 'collision'
    df.loc[df['issue_reported'] == 'collisn/ lvng scn', 'issue_reported'] = 'collision'
    df.loc[df['issue_reported'] == 'collision/private property', 'issue_reported'] = 'collision on private property'
    df.loc[df['issue_reported'] == 'fleet acc/ fatal', 'issue_reported'] = 'fleet accident'
    df.loc[df['issue_reported'] == 'fleet acc/ injury', 'issue_reported'] = 'fleet accident'

    cols_to_remove = ['status', 'status_date']
    df = df.drop(columns=cols_to_remove)

    df = df.dropna(subset=['latitude', 'longitude', 'location'], how='all')

    # Fill missing location values with combined latitude and longitude
    # df.loc[df['location'].isna(), 'location'] = df.apply(lambda row: f"({row['latitude']}, {row['longitude']})", axis=1)
    df['location'] = df.apply(combine_lat_lon, axis=1)
    df = df[~((df['latitude'] < -90) | (df['latitude'] > 90))]

    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['date_time'] = pd.to_datetime(df['date_time'])
    df['weekday'] = df['date_time'].dt.day_name()
    df['date'] = df['date_time'].dt.date
    df['time'] = df['date_time'].dt.time

    # Converted to int to be a primary key - represented as the number of seconds since 1/1/1970
    df['timestamp'] = df['timestamp'].astype(int)

    return df

def get_new_data(df, get_date):
    yesterday = get_yesterday_date(get_date)
    df = df.sort_values(by=['timestamp'], ascending=True)
    data_to_append = df[(df['date_time'].dt.date == yesterday)]
    return data_to_append

# def save_new_data_to_csv(data_to_append, get_date):
#     filename = get_file_path(get_date)
#     if not data_to_append.empty:
#         data_to_append.to_csv(filename, encoding='utf-8', index=False)

def save_new_data_to_csv(data_to_append, get_date):
    filename = os.path.join(config.CSV_DIR, get_file_path(get_date))
    if not data_to_append.empty:
        data_to_append.to_csv(filename, encoding='utf-8', index=False)

def main(get_date):
    data_json = import_data()
    df = transform_data(data_json)
    data_to_append = get_new_data(df, get_date)
    save_new_data_to_csv(data_to_append, get_date)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True, type=str)
    args = parser.parse_args()
    main(args.date)