import csv
from typing import List, Dict

def export_to_csv(filename: str, data: List[Dict[str, str]]):
    with open(filename, mode='w', newline='', encoding='utf-8') as csv_file:
        if not data:
            return
        writer = csv.DictWriter(csv_file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)