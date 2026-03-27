import psutil
import datetime

def collect_snapshot():
    print(f"\n📊 Process Snapshot — {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'PID':<10} {'Name':<25} {'CPU %':<10} {'Memory %':<10} {'Status'}")
    print("-" * 65)

    processes = []

    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
        try:
            info = proc.info
            # Skip any process with missing fields
            if None in (info['pid'], info['name'], info['cpu_percent'], info['memory_percent'], info['status']):
                continue
            processes.append(info)
            print(f"{info['pid']:<10} {info['name'][:24]:<25} {info['cpu_percent']:<10} {round(info['memory_percent'], 2):<10} {info['status']}")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    print(f"\n✅ Total processes captured: {len(processes)}")
    return processes

if __name__ == "__main__":
    collect_snapshot()