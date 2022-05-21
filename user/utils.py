import csv
import time


def create_conflict_report(report_type, data):
    if report_type == 'SubscriberSMS':
        filename = f'reports/subscribersms_conflicts_{time.strftime("%Y%m%d-%H%M%S")}.csv'
    else:
        filename = f'reports/subscriber_conflicts_{time.strftime("%Y%m%d-%H%M%S")}.csv'

    csv_columns = ['id', 'email', 'reason']

    with open(filename, 'w', encoding='UTF8') as f:
        writer = csv.DictWriter(f, fieldnames=csv_columns)
        writer.writeheader()

        for item in data:
            writer.writerow(item)
