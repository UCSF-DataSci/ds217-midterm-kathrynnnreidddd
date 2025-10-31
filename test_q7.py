import sys
from pathlib import Path
import pandas as pd

OK,BAD="ok","bad"
print("\n Q7 checks...\n")

src = Path("data/clinical_trial_raw.csv")
site_csv = Path("output/q7_site_summary.csv")
interv_csv = Path("output/q7_intervention_comparison.csv")
report = Path("output/q7_analysis_report.txt")

# A) Existence
print(OK,"q7_site_summary.csv exists" if site_csv.exists() else BAD+" missing q7_site_summary.csv")
print(OK,"q7_intervention_comparison.csv exists" if interv_csv.exists() else BAD+" missing q7_intervention_comparison.csv")
print(OK,"q7_analysis_report.txt exists" if report.exists() else BAD+" missing q7_analysis_report.txt")

if not (site_csv.exists() and interv_csv.exists() and report.exists()):
    sys.exit(0)

# B) Load
try:
    df_in = pd.read_csv(src) if src.exists() else None
    site = pd.read_csv(site_csv)
    interv = pd.read_csv(interv_csv)
    print(OK,"loaded summary CSVs")
except Exception as e:
    print(BAD,"failed to read CSVs:", e); sys.exit(0)

# C) Site summary structure
cols_lower = [c.lower() for c in site.columns]
has_site_col = "site" in cols_lower
print(OK,"site summary has 'site' column" if has_site_col else BAD+" 'site' column missing")
n_sites = site.shape[0]
print(OK,f"site summary has 5 rows (got {n_sites})" if n_sites==5 else BAD+f" expected 5 rows, got {n_sites}")

# D) Aggregated (not raw) sanity: far fewer rows than input
if df_in is not None:
    aggregated = site.shape[0] < df_in.shape[0]
    print(OK,"site summary looks aggregated" if aggregated else BAD+" site summary looks like raw data")

# E) Intervention comparison structure
interv_cols = [c.lower() for c in interv.columns]
has_group_col = any(k in interv_cols for k in ["intervention","group","arm"])
print(OK,"intervention comparison has group column" if has_group_col else BAD+" missing group/arm column")
# at least 2 groups
n_groups = None
for k in ["intervention","group","arm"]:
    if k in interv_cols:
        n_groups = interv[k if k in interv.columns else [c for c in interv.columns if c.lower()==k][0]].nunique()
        break
if n_groups is not None:
    print(OK,f"intervention comparison has ≥2 groups (got {n_groups})" if n_groups>=2 else BAD+f" only {n_groups} group")

# F) Report content
print(OK,"analysis report has text" if report.stat().st_size>0 else BAD+" analysis report is empty")

print("\n Q7 checks complete.\n")
