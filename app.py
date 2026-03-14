from flask import Flask, render_template
import psutil
import platform
import socket
from datetime import datetime

app = Flask(__name__)

def get_system_info():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    net_io = psutil.net_io_counters()

    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    top_processes = sorted(
        processes,
        key=lambda p: (p['cpu_percent'] or 0, p['memory_percent'] or 0),
        reverse=True
    )[:10]

    alerts = []
    if cpu_usage > 80:
        alerts.append(f"High CPU usage detected: {cpu_usage}%")
    if memory.percent > 80:
        alerts.append(f"High memory usage detected: {memory.percent}%")
    if disk.percent > 85:
        alerts.append(f"High disk usage detected: {disk.percent}%")

    return {
        "hostname": socket.gethostname(),
        "platform": platform.system() + " " + platform.release(),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cpu_usage": cpu_usage,
        "memory_total": round(memory.total / (1024**3), 2),
        "memory_used": round(memory.used / (1024**3), 2),
        "memory_percent": memory.percent,
        "disk_total": round(disk.total / (1024**3), 2),
        "disk_used": round(disk.used / (1024**3), 2),
        "disk_percent": disk.percent,
        "bytes_sent": round(net_io.bytes_sent / (1024**2), 2),
        "bytes_recv": round(net_io.bytes_recv / (1024**2), 2),
        "top_processes": top_processes,
        "alerts": alerts
    }

@app.route("/")
def index():
    data = get_system_info()
    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(debug=True, port=5002)
