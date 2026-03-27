import psutil
import datetime
import csv
import os

CSV_FILE = "baseline.csv"

def save_snapshot():
    snapshot_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    rows = []

    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
        try:
            info = proc.info
            if None in (info['pid'], info['name'], info['cpu_percent'], info['memory_percent'], info['status']):
                continue
            rows.append({
                'timestamp': snapshot_time,
                'pid': info['pid'],
                'name': info['name'],
                'cpu_percent': info['cpu_percent'],
                'memory_percent': round(info['memory_percent'], 2),
                'status': info['status']
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['timestamp', 'pid', 'name', 'cpu_percent', 'memory_percent', 'status'])
        if not file_exists:
            writer.writeheader()
        writer.writerows(rows)

    print(f"✅ Snapshot saved at {snapshot_time} — {len(rows)} processes logged to {CSV_FILE}")

if __name__ == "__main__":
    save_snapshot()