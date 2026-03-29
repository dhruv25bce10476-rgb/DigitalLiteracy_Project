import subprocess
import threading
import http.server
import os
import time
import sys

PORT = 18923
HTML_FILE = "Project_Report.html"
PDF_FILE = "Project_Report.pdf"
SERVE_DIR = r"d:\screenshots"

# Chrome path
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # suppress logs

def start_server():
    os.chdir(SERVE_DIR)
    httpd = http.server.HTTPServer(("127.0.0.1", PORT), QuietHandler)
    httpd.serve_forever()

# Start HTTP server in background
server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()
time.sleep(1)

url = f"http://127.0.0.1:{PORT}/{HTML_FILE}"
output_path = os.path.join(SERVE_DIR, PDF_FILE)

print(f"Converting {url} to PDF...")

result = subprocess.run([
    CHROME,
    "--headless",
    "--disable-gpu",
    "--no-sandbox",
    "--run-all-compositor-stages-before-draw",
    "--virtual-time-budget=5000",
    f"--print-to-pdf={output_path}",
    "--print-to-pdf-no-header",
    url
], capture_output=True, text=True, timeout=30)

if result.returncode == 0 and os.path.exists(output_path):
    size = os.path.getsize(output_path)
    print(f"SUCCESS! PDF created: {output_path} ({size:,} bytes)")
else:
    print(f"Chrome stdout: {result.stdout}")
    print(f"Chrome stderr: {result.stderr}")
    print(f"Return code: {result.returncode}")
    sys.exit(1)
