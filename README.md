# PulseWatch

PulseWatch is an advanced system monitor dashboard built with Flask and psutil. It provides live visibility into CPU, memory, disk, and network usage, along with system alerts and top running processes.

## Features
- Live CPU, RAM, and disk monitoring
- Network I/O stats
- Top running processes
- Auto-refresh dashboard
- System alerts for high usage
- Clean responsive UI

## Tech Stack
- Python
- Flask
- psutil
- HTML/CSS

## Run Locally

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
