from flask import Flask, render_template
import psutil
import socket
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def dashboard():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    hostname = socket.gethostname()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return render_template(
        "index.html",
        cpu=cpu,
        memory=memory,
        hostname=hostname,
        time=current_time
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

