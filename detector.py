import psutil
import csv
import datetime
from collections import defaultdict

CSV_FILE = "baseline.csv"
CPU_THRESHOLD = 10.0    # flag if CPU % is higher than this
MEM_THRESHOLD = 2.0     # flag if memory % is higher than this

def load_baseline():
    baseline = defaultdict(list)
    with open(CSV_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row['name']
            baseline[name].append({
                'cpu': float(row['cpu_percent']),
                'mem': float(row['memory_percent'])
            })
    return baseline

def get_averages(baseline):
    averages = {}
    for name, snapshots in baseline.items():
        avg_cpu = sum(s['cpu'] for s in snapshots) / len(snapshots)
        avg_mem = sum(s['mem'] for s in snapshots) / len(snapshots)
        averages[name] = {'avg_cpu': avg_cpu, 'avg_mem': avg_mem}
    return averages

def detect_anomalies(averages):
    print(f"\n🔍 Anomaly Scan — {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'PID':<10} {'Name':<25} {'CPU %':<10} {'Mem %':<10} {'Reason'}")
    print("-" * 75)

    anomalies = []

    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            info = proc.info
            if None in (info['pid'], info['name'], info['cpu_percent'], info['memory_percent']):
                continue

            name = info['name']
            cpu = info['cpu_percent']
            mem = round(info['memory_percent'], 2)
            reasons = []

            if cpu > CPU_THRESHOLD:
                reasons.append(f"High CPU ({cpu}%)")

            if mem > MEM_THRESHOLD:
                reasons.append(f"High Mem ({mem}%)")

            if name in averages:
                avg_cpu = averages[name]['avg_cpu']
                avg_mem = averages[name]['avg_mem']
                if avg_cpu > 0 and cpu > avg_cpu * 3:
                    reasons.append(f"CPU spike vs baseline ({avg_cpu:.2f}% avg)")
                if avg_mem > 0 and mem > avg_mem * 2:
                    reasons.append(f"Mem spike vs baseline ({avg_mem:.2f}% avg)")
            else:
                reasons.append("New/unknown process")

            if reasons:
                anomalies.append(info)
                print(f"{info['pid']:<10} {name[:24]:<25} {cpu:<10} {mem:<10} {', '.join(reasons)}")

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    if not anomalies:
        print("✅ No anomalies detected — system looks normal!")
    else:
        print(f"\n⚠️  {len(anomalies)} anomalous process(es) flagged.")

if __name__ == "__main__":
    averages = get_averages(load_baseline())
    detect_anomalies(averages)