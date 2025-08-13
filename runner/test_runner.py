import subprocess
import os
from config import REPORT_DIR

class TestRunner:
    def __init__(self):
        os.makedirs(REPORT_DIR, exist_ok=True)

    def run_tests(self, test_path: str):
        report_file = os.path.join(REPORT_DIR, "report.html")
        subprocess.run([
            "pytest", test_path, "--html=" + report_file, "--self-contained-html"
        ])
        print(f"Test execution complete. Report saved at {report_file}")
