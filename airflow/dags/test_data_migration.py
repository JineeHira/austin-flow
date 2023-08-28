import unittest
from unittest.mock import patch, Mock
from io import StringIO
from pathlib import Path
from sqlalchemy.orm import Session
from model import Connection
from data_migration import main
import textwrap

class TestInitializeTable(unittest.TestCase):

    @patch('model.Connection')
    @patch('data_migration.Path')
    def test_main(self, mock_Path, mock_Connection):
        mock_connection_instance = mock_Connection.return_value
        mock_session = Mock(spec=Session)
        mock_connection_instance.get_session.return_value = mock_session

        main('postgresql+psycopg2://airflow:airflow@postgres/airflow')

        mock_Path.assert_called_once_with('/Users/jinee.hira/Dropbox/virtual_envs/austin-flow/airflow/dags/data')
        mock_Path.return_value.mkdir.assert_called_once_with(parents=True, exist_ok=True)
        mock_connection_instance.get_session.assert_called_once()
        
        expected_sql = textwrap.dedent('''\
            CREATE TABLE IF NOT EXISTS traffic_report (
                timestamp INT PRIMARY KEY,
                traffic_report_id VARCHAR(255), 
                date_time TIMESTAMP, 
                issue_reported VARCHAR(20), 
                location POINT, 
                latitude DECIMAL, 
                longitude DECIMAL, 
                address VARCHAR(255),
                weekday VARCHAR(15),
                date DATE,
                time TIME)
        ''')
        mock_session.execute.assert_called_once_with(expected_sql)
        mock_session.commit.assert_called_once()
        mock_session.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()

