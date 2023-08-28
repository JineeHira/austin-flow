import os
import unittest
from unittest.mock import patch
from io import StringIO
import pandas as pd
from datetime import datetime, timedelta
from traffic_script import combine_lat_lon, import_data, transform_data, get_new_data, save_new_data_to_csv

class TestTrafficScript(unittest.TestCase):

    def setUp(self):
        self.sample_data = {
            'data': [
                {
                    'Traffic Report ID': 'C163BCD1CF90C984E9EDA4DBA311BCA369A7D1A1_15288',
                    'Published Date': '06/13/2018 06:35:59 AM +0000',
                    'Issue Reported': 'Crash Service',
                    'Location': '(30.283797,-97.741906)',
                    'Latitude': 30.283797,
                    'Longitude': -97.741906,
                    'Address': 'W 21ST ST & GUADALUPE ST',
                    'Status': 'ARCHIVED',
                    'Status Date': '06/13/2018 09:00:03 AM +0000'
                }
            ]
        }

    def test_combine_lat_lon(self):
        row = {'location': None, 'latitude': 30.283797, 'longitude': -97.741906}
        result = combine_lat_lon(row)
        self.assertEqual(result, '(30.283797, -97.741906)')

        row = {'location': 'Sample Location', 'latitude': 30.339593, 'longitude': -97.700963}
        result = combine_lat_lon(row)
        self.assertEqual(result, 'Sample Location')

    @patch('traffic_script.requests.get')
    def test_import_data(self, mock_get):
        mock_get.return_value.json.return_value = self.sample_data
        data = import_data()
        self.assertEqual(data, self.sample_data)

    def test_transform_data(self):
        transformed_data = transform_data(self.sample_data)
        self.assertIsInstance(transformed_data, pd.DataFrame)

    def test_get_new_data(self):
        # Transform the data
        transformed_data = transform_data(self.sample_data)
        
        # Get yesterday's date
        yesterday = (datetime.now() - timedelta(days=1)).date()
        # Convert yesterday to string
        yesterday_str = yesterday.strftime('%Y-%m-%d')
        
        # Get new data
        data_to_append = get_new_data(transformed_data, yesterday_str)
        self.assertIsInstance(data_to_append, pd.DataFrame)

    def test_save_new_data_to_csv(self):
        transformed_data = transform_data(self.sample_data)
        yesterday = (datetime.now() - timedelta(days=1)).date()
        yesterday_str = yesterday.strftime('%Y-%m-%d')
        
        # Define the file path for CSV
        csv_dir = '/Users/jinee.hira/Dropbox/virtual_envs/austin-flow/airflow/dags/data'
        csv_filename = f'dailytraffic_{yesterday_str}.csv'
        csv_path = os.path.join(csv_dir, csv_filename)
        
        # Redirect stdout to capture print statements
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            save_new_data_to_csv(transformed_data, yesterday_str)
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, '')  # Check if there are no print statements
            
            # Check if the CSV file was created and contains data
            try:
                csv_data = pd.read_csv(csv_path)
                self.assertFalse(csv_data.empty, msg="CSV file is empty")
            except FileNotFoundError:
                self.fail(f"CSV file '{csv_filename}' was not created")

if __name__ == '__main__':
    unittest.main()





