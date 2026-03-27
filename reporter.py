import psutil
import csv
import datetime
from collections import defaultdict

CSV_FILE = "baseline.csv"
LOG_FILE = "anomaly_log.txt"
CPU_THRESHOLD = 10.0
MEM_THRESHOLD = 2.0

def load_baseline():
    baseline = defaultdict(list)
    with open(CSV_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            baseline[row['name']].append({
                'cpu': float(row['cpu_percent']),
                'mem': float(row['memory_percent'])
            })
    return baseline

def get_averages(baseline):
    averages = {}
    for name, snapshots in baseline.items():
        averages[name] = {
            'avg_cpu': sum(s['cpu'] for s in snapshots) / len(snapshots),
            'avg_mem': sum(s['mem'] for s in snapshots) / len(snapshots)
        }
    return averages

def run_and_report(averages):
    scan_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
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
                if averages[name]['avg_cpu'] > 0 and cpu > averages[name]['avg_cpu'] * 3:
                    reasons.append(f"CPU spike vs baseline ({averages[name]['avg_cpu']:.2f}% avg)")
                if averages[name]['avg_mem'] > 0 and mem > averages[name]['avg_mem'] * 2:
                    reasons.append(f"Mem spike vs baseline ({averages[name]['avg_mem']:.2f}% avg)")
            else:
                reasons.append("New/unknown process")

            if reasons:
                anomalies.append((info['pid'], name, cpu, mem, ', '.join(reasons)))

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    # Print to terminal
    print(f"\n🔍 Anomaly Report — {scan_time}")
    print(f"{'PID':<10} {'Name':<25} {'CPU %':<10} {'Mem %':<10} {'Reason'}")
    print("-" * 75)
    if anomalies:
        for pid, name, cpu, mem, reason in anomalies:
            print(f"{pid:<10} {name[:24]:<25} {cpu:<10} {mem:<10} {reason}")
        print(f"\n⚠️  {len(anomalies)} anomalous process(es) flagged.")
    else:
        print("✅ No anomalies detected.")

    # Write to log file
    with open(LOG_FILE, 'a') as f:
        f.write(f"\n{'='*75}\n")
        f.write(f"SCAN TIME: {scan_time}\n")
        f.write(f"ANOMALIES FOUND: {len(anomalies)}\n")
        f.write(f"{'='*75}\n")
        if anomalies:
            f.write(f"{'PID':<10} {'Name':<25} {'CPU %':<10} {'Mem %':<10} {'Reason'}\n")
            f.write(f"{'-'*75}\n")
            for pid, name, cpu, mem, reason in anomalies:
                f.write(f"{pid:<10} {name[:24]:<25} {cpu:<10} {mem:<10} {reason}\n")
        else:
            f.write("No anomalies detected.\n")

    print(f"\n📝 Report saved to {LOG_FILE}")

if __name__ == "__main__":
    averages = get_averages(load_baseline())
    run_and_report(averages)