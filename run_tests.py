import subprocess
import sys

# Path to virtual environment Python
venv_path = ".\\venv\\Scripts\\python.exe"

try:
    # Run pytest without warnings
    result = subprocess.run([venv_path, "-m", "pytest", "-v", "-p", "no:warnings"], check=True)
    sys.exit(0)
except subprocess.CalledProcessError:
    sys.exit(1)
