# TODO: Add shebang line: #!/bin/bash
# Assignment 5, Question 8: Pipeline Automation Script
# Run the clinical trial data analysis pipeline

# NOTE: This script assumes Q1 has already been run to create directories and generate the dataset
# NOTE: Q2 (q2_process_metadata.py) is a standalone Python fundamentals exercise, not part of the main pipeline
# NOTE: Q3 (q3_data_utils.py) is a library imported by the notebooks, not run directly
# NOTE: The main pipeline runs Q4-Q7 notebooks in order

set -o pipefail

LOGDIR="reports"
LOGFILE="${LOGDIR}/pipeline_log.txt"

mkdir -p "${LOGDIR}"

{
  echo "=============================================="
  echo "Pipeline started: $(date)"
  echo "Working directory: $(pwd)"
  echo "=============================================="
} > "${LOGFILE}"

echo "[INFO] Starting clinical trial data pipeline..." | tee -a "${LOGFILE}"
echo "Starting clinical trial data pipeline..." > reports/pipeline_log.txt

# TODO: Run analysis notebooks in order (q4-q7) using nbconvert with error handling
# Use either `$?` or `||` operator to check exit codes and stop on failure
# Add a log entry for each notebook execution or failure
# jupyter nbconvert --execute --to notebook q4_exploration.ipynb

if ! command -v jupyter >/dev/null 2>&1; then
  echo "[ERROR] 'jupyter' command not found. Please install Jupyter and try again." | tee -a "${LOGFILE}"
  exit 1
fi

shopt -s nullglob
NOTEBOOKS=(q4_*.ipynb q5_*.ipynb q6_*.ipynb q7_*.ipynb)
shopt -u nullglob

if [ ${#NOTEBOOKS[@]} -eq 0 ]; then
  echo "[ERROR] No Q4–Q7 notebooks found (expected files like q4_*.ipynb, q5_*.ipynb, q6_*.ipynb, q7_*.ipynb)." | tee -a "${LOGFILE}"
  exit 1
fi

for nb in "${NOTEBOOKS[@]}"; do
  echo "[INFO] Running notebook: ${nb}" | tee -a "${LOGFILE}"
  jupyter nbconvert --execute --to notebook --inplace "${nb}" >> "${LOGFILE}" 2>&1 \
    || { echo "[ERROR] Execution failed for ${nb}. Stopping pipeline." | tee -a "${LOGFILE}"; exit 1; }
  echo "[SUCCESS] Completed: ${nb}" | tee -a "${LOGFILE}"
done

echo "[INFO] All notebooks completed successfully." | tee -a "${LOGFILE}"
echo "Pipeline finished: $(date)" | tee -a "${LOGFILE}"
echo "Pipeline complete!" >> reports/pipeline_log.txt
