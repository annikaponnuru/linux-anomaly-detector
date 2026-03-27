import time
import datetime
from collector import collect_snapshot
from baseline import save_snapshot
from reporter import load_baseline, get_averages, run_and_report

def main():
    print("=" * 65)
    print("🛡️  Linux Process Behavior Anomaly Detector")
    print(f"   Started at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 65)

    # Stage 1: Collect a live snapshot
    print("\n📊 Stage 1: Collecting live process snapshot...")
    collect_snapshot()

    # Stage 2: Save to baseline
    print("\n💾 Stage 2: Saving snapshot to baseline...")
    save_snapshot()

    # Small delay so CPU readings stabilize
    print("\n⏳ Waiting 2 seconds for readings to stabilize...")
    time.sleep(2)

    # Stage 3 & 4: Detect anomalies and save report
    print("\n🔍 Stage 3 & 4: Running anomaly detection and saving report...")
    averages = get_averages(load_baseline())
    run_and_report(averages)

    print("\n✅ Done! Check anomaly_log.txt for the full report.")
    print("=" * 65)

if __name__ == "__main__":
    main()