#!/usr/bin/env bash
airflow db init
airflow users create -r Admin -u admin -f admin -l admin -p admin2023 -e jinee.hira@gmail.com
airflow webserver