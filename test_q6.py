import sys
from pathlib import Path
import pandas as pd

OK, BAD = "ok","bad"

print("\n Q6 checks...\n")

src = Path("data/clinical_trial_raw.csv")
out = Path("output/q6_transformed_data.csv")

# A) Files exist
print(OK,"data file exists" if src.exists() else BAD+" data/clinical_trial_raw.csv missing")
print(OK,"output file exists" if out.exists() else BAD+" output/q6_transformed_data.csv missing")

if not (src.exists() and out.exists()):
    sys.exit(0)

# B) Load both
try:
    df_in  = pd.read_csv(src)
    df_out = pd.read_csv(out)
    print(OK,"loaded input and transformed CSVs")
except Exception as e:
    print(BAD,"failed to read CSVs:", e)
    sys.exit(0)

# C) More columns than input
more_cols = df_out.shape[1] > df_in.shape[1]
print(OK,"transformed has more columns than input" if more_cols else BAD+" no new features detected")

# D) Look for binned/categorical columns
cands_bin = [c for c in df_out.columns if any(k in c.lower() for k in
                 ["age_group","agegroup","bmi_category","bmi_cat","_bin","_bins","bucket","group"])]
print(OK,f"found binned/categorical column(s): {cands_bin}" if cands_bin else BAD+" no binned/categorical columns found")

# E) Look for calculated columns
cands_calc = [c for c in df_out.columns if any(k in c.lower() for k in
                  ["ratio","score","index","_calc","derived"])]
print(OK,f"found calculated column(s): {cands_calc}" if cands_calc else BAD+" no calculated columns found")

print("\n ok Q6 checks complete.\n")
