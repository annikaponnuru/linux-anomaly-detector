# 🛡️ Linux Process Behavior Anomaly Detector

A Python-based security monitoring tool that collects OS-level telemetry and detects unusual process behavior on Linux/macOS systems. Built to explore the intersection of operating systems and security analytics.

---

## 📌 Overview

This tool monitors running processes on a system, builds a behavioral baseline over time, and flags any processes that deviate significantly from normal — such as unexpected CPU spikes, memory surges, or unknown processes appearing on the system.

This project was built to strengthen skills in:
- Linux/macOS OS internals and process management
- Python scripting for security automation
- Behavioral baseline modeling and anomaly detection
- Security monitoring and audit logging

---

## 🗂️ Project Structure

```
linux-anomaly-detector/
├── main.py          # Runs the full pipeline in one command
├── collector.py     # Stage 1: Collects a live snapshot of all running processes
├── baseline.py      # Stage 2: Saves snapshots to a CSV to build a behavioral baseline
├── detector.py      # Stage 3: Compares live data against the baseline and flags anomalies
├── reporter.py      # Stage 4: Outputs flagged anomalies to terminal and saves an audit log
```

---

## ⚙️ How It Works

**Stage 1 — Process Collector**
Captures a real-time snapshot of all running processes including PID, name, CPU usage, memory usage, and status using Python's `psutil` library.

**Stage 2 — Baseline Builder**
Saves process snapshots to a CSV file over time to build a picture of "normal" system behavior for each process.

**Stage 3 — Anomaly Detector**
Compares live process data against the baseline averages. Flags processes that exceed CPU/memory thresholds or show significant spikes compared to their historical averages.

**Stage 4 — Reporter**
Prints a formatted anomaly report to the terminal and appends it to a persistent `anomaly_log.txt` audit file with timestamps.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.x
- `psutil` library

### Installation

```bash
git clone https://github.com/annikaponnuru/linux-anomaly-detector.git
cd linux-anomaly-detector
pip3 install psutil
```

### Usage

Run the full pipeline with one command:
```bash
python3 main.py
```

Or run each stage individually:
```bash
python3 collector.py   # View live process snapshot
python3 baseline.py    # Save a snapshot to baseline
python3 detector.py    # Run anomaly detection
python3 reporter.py    # Run detection and save audit log
```

> **Tip:** Run `python3 baseline.py` several times before running the detector to build a more accurate baseline.

---

## 📊 Example Output

```
🔍 Anomaly Report — 2026-03-27 02:51:27
PID        Name                      CPU %      Mem %      Reason
---------------------------------------------------------------------------
73055      Google Chrome Helper (Re  18.3       3.54       High CPU (18.3%), High Mem (3.54%), CPU spike vs baseline
58289      Google Chrome Helper (Re  0.0        4.21       High Mem (4.21%), Mem spike vs baseline (0.57% avg)
73898      Code Helper (Renderer)    4.1        1.82       Mem spike vs baseline (0.69% avg)

⚠️  17 anomalous process(es) flagged.
📝 Report saved to anomaly_log.txt
```

---

## 🔧 Detection Thresholds

| Metric | Threshold |
|---|---|
| CPU usage | > 10% |
| Memory usage | > 2% |
| CPU spike vs baseline | > 3x average |
| Memory spike vs baseline | > 2x average |

Thresholds can be adjusted in `reporter.py` and `detector.py`.

---

## 🛠️ Built With

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=flat&logo=linux&logoColor=black)
![macOS](https://img.shields.io/badge/macOS-000000?style=flat&logo=apple&logoColor=white)

---

## 🚧 Planned Improvements

- [ ] Continuous monitoring mode with scheduled scans
- [ ] Desktop/email alerts for critical anomalies
- [ ] Data visualization dashboard for process trends
- [ ] Export reports to JSON format

---

## 👩‍💻 Author

**Annika Ponnuru** — CS Student @ Toronto Metropolitan University  
[GitHub](https://github.com/annikaponnuru) · [LinkedIn](https://linkedin.com/in/annikaponnuru)
