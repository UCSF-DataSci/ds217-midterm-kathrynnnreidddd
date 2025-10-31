
import os

from pathlib import Path

data_dir = Path("data")

output_dir = Path("output")

reports_dir = Path("reports")

setup_script = Path("q1_setup_project.sh")

raw_csv = data_dir / "clinical_trial_raw.csv"

structure_txt = reports_dir / "directory_structure.txt"

print(" Checking Q1: Project Setup Script...\n")
print(" q1_setup_project.sh exists" if setup_script.exists() else " q1_setup_project.sh is missing")
print(" Script is executable" if os.access(setup_script, os.X_OK) else " Script not executable (run: chmod +x q1_setup_project.sh)")
try:
    with open(setup_script, "r") as f:
        first = f.readline().strip()
        if first.startswith("#!/bin/bash") or first.startswith("#!/bin/sh"):
            print(" Script has valid shebang line")
        else:
            print(f" Invalid shebang: {first}")
except FileNotFoundError:
    print(" Cannot open script to check shebang")
Ctrl + C
cat > test_q1.py <<'PY'
import os
from pathlib import Path

data_dir = Path("data")
output_dir = Path("output")
reports_dir = Path("reports")
setup_script = Path("q1_setup_project.sh")
raw_csv = data_dir / "clinical_trial_raw.csv"
structure_txt = reports_dir / "directory_structure.txt"

print(" Checking Q1: Project Setup Script...\n")

print(" q1_setup_project.sh exists" if setup_script.exists() else "q1_setup_project.sh is missing")
print("Script is executable" if os.access(setup_script, os.X_OK) else "Script not executable (run: chmod +x q1_setup_project.sh)")

try:
    with open(setup_script, "r") as f:
        first = f.readline().strip()
        if first.startswith("#!/bin/bash") or first.startswith("#!/bin/sh"):
            print("Script has valid shebang line")
        else:
            print(f" Invalid shebang: {first}")
except FileNotFoundError:
    print("Cannot open script to check shebang")

for d in [data_dir, output_dir, reports_dir]:
    print(f"Directory '{d}/' exists" if d.exists() else f" Missing directory '{d}/'")

print("clinical_trial_raw.csv exists" if raw_csv.exists() else " clinical_trial_raw.csv missing in data/")
print("directory_structure.txt exists" if structure_txt.exists() else "directory_structure.txt missing in reports/")

print("\n Q1 checks complete.")
