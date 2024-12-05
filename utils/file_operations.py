import csv
import os
import time

def initialize_csv(file_path):
    if not os.path.exists(file_path):
        with open(file_path, mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["Timestamp", "URL", "Status Code"])

def write_failed_api_to_csv(file_path, url, status_code):
    with open(file_path, mode='a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), url, status_code])
