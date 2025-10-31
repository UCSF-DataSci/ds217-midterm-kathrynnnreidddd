import os, sys, traceback
from pathlib import Path

OK, BAD = "ok", "bad"

print("\n Q3 checks...\n")

# ---- Imports ----
try:
    import pandas as pd
    import numpy as np
    import q3_data_utils as utils
    print(OK, "Imported pandas, numpy, q3_data_utils")
except Exception as e:
    print(BAD, "Import failed:", e)
    sys.exit(0)

data_path = Path("data/clinical_trial_raw.csv")
if not data_path.exists():
    print(BAD, "data/clinical_trial_raw.csv is missing — some checks will use a synthetic DataFrame.")

def show(result, ok_msg, bad_msg):
    print(OK, ok_msg) if result else print(BAD, bad_msg)

# ---- 1) load_data ----
try:
    if data_path.exists():
        df = utils.load_data(str(data_path))
    else:
        # fallback synthetic
        df = pd.DataFrame({
            "age":[20,35,70,70],
            "site":["Site A","Site B","Site A","Site C"],
            "enrollment_date":["2025-01-01","2025-02-01","2025-03-01","2025-03-05"]
        })
    show(isinstance(df, pd.DataFrame), "load_data returns DataFrame", "load_data did not return DataFrame")
    show(len(df) > 0 and len(df.columns) > 0, "DataFrame has rows and columns", "DataFrame is empty")
except Exception as e:
    print(BAD, "load_data raised:", e)

# ---- 2) clean_data ----
try:
    demo = pd.DataFrame({"x":[1,1,-999], "y":[0,0,0]})
    cleaned = utils.clean_data(demo.copy(), remove_duplicates=True, sentinel_value=-999)
    show(isinstance(cleaned, pd.DataFrame), "clean_data returns DataFrame", "clean_data did not return DataFrame")
    # sentinel replaced if present
    sentinel_ok = (-999 not in cleaned.values)
    show(sentinel_ok, "clean_data replaced sentinel with NaN", "sentinel -999 still present")
except Exception as e:
    print(BAD, "clean_data raised:", e)

# ---- 3) detect_missing ----
try:
    s = utils.detect_missing(df)
    show(isinstance(s, pd.Series), "detect_missing returns Series", "detect_missing did not return Series")
    show(len(s) == len(df.columns), "detect_missing has one count per column", "Series length != # of cols")
except Exception as e:
    print(BAD, "detect_missing raised:", e)

# ---- 4) fill_missing ----
try:
    t = pd.DataFrame({"col":[1, np.nan, 3]})
    filled_mean = utils.fill_missing(t.copy(), "col", "mean")
    show(filled_mean["col"].isna().sum()==0, "fill_missing handles 'mean/median'", "fill_missing failed for mean/median")
    filled_ffill = utils.fill_missing(pd.DataFrame({"col":[1, np.nan, 3]}), "col", "ffill")
    show(filled_ffill["col"].isna().sum()==0, "fill_missing handles 'ffill'", "fill_missing failed for ffill")
except Exception as e:
    print(BAD, "fill_missing raised:", e)

# ---- 5) filter_data ----
try:
    base = df.copy()
    # Pick columns that likely exist; otherwise create a minimal one
    if not {"age","site"}.issubset(base.columns):
        base = pd.DataFrame({"age":[10,25,40,80], "site":["Site A","Site B","Site A","Site C"]})
    f1 = utils.filter_data(base, [{'column':'age','condition':'greater_than','value':18}])
    show(isinstance(f1, pd.DataFrame), "filter_data applies single filter", "single filter failed")

    f2 = utils.filter_data(base, [
        {'column':'age','condition':'greater_than','value':18},
        {'column':'site','condition':'equals','value':'Site A'}
    ])
    ok_multi = isinstance(f2, pd.DataFrame) and (len(f2)==0 or ((f2["age"]>18).all() and (f2["site"]=="Site A").all()))
    show(ok_multi, "filter_data applies multiple filters", "multiple filters failed")

    f3 = utils.filter_data(base, [{'column':'age','condition':'in_range','value':[18,65]}])
    ok_ir = isinstance(f3, pd.DataFrame) and (len(f3)==0 or ((f3["age"]>=18)&(f3["age"]<=65)).all())
    show(ok_ir, "filter_data handles in_range", "in_range failed")

    f4 = utils.filter_data(base, [{'column':'site','condition':'in_list','value':['Site A','Site B']}])
    ok_list = isinstance(f4, pd.DataFrame) and (len(f4)==0 or f4["site"].isin(['Site A','Site B']).all())
    show(ok_list, "filter_data handles in_list", "in_list failed")
except Exception as e:
    print(BAD, "filter_data raised:", e)

# ---- 6) transform_types ----
try:
    temp = df.copy()
    type_map = {}
    if "enrollment_date" in temp.columns: type_map["enrollment_date"] = "datetime"
    if "site" in temp.columns: type_map["site"] = "category"
    if not type_map:  # fallback
        temp = pd.DataFrame({"d":["2025-01-01","2025-02-01"], "c":["A","B"]})
        type_map = {"d":"datetime", "c":"category"}
    typed = utils.transform_types(temp, type_map)
    ok = True
    for col, tgt in type_map.items():
        if tgt=="datetime": ok &= pd.api.types.is_datetime64_any_dtype(typed[col])
        if tgt=="category": ok &= (str(typed[col].dtype)=="category")
        if tgt=="numeric": ok &= pd.api.types.is_numeric_dtype(typed[col])
    show(ok, "transform_types converts to requested dtypes", "transform_types failed")
except Exception as e:
    print(BAD, "transform_types raised:", e)

# ---- 7) create_bins ----
try:
    base = df.copy()
    if "age" not in base.columns:
        base = pd.DataFrame({"age":[20,45,70]})
    b1 = utils.create_bins(base, "age", [0,40,60,120], ["<40","40-59","60+"])
    show(isinstance(b1, pd.DataFrame) and (len(b1.columns) > len(base.columns)),
         "create_bins adds a binned column", "create_bins failed (no new column)")
    b2 = utils.create_bins(base, "age", [0,40,60,120], ["<40","40-59","60+"], new_column="age_groups")
    show("age_groups" in b2.columns, "create_bins respects new_column name", "new_column not created")
except Exception as e:
    print(BAD, "create_bins raised:", e)

# ---- 8) summarize_by_group ----
try:
    base = df.copy()
    if not {"site","age"}.issubset(base.columns):
        base = pd.DataFrame({"site":["Site A","Site A","Site B"],"age":[30,40,50]})
    s1 = utils.summarize_by_group(base, "site", {"age":"mean"})
    show(isinstance(s1, pd.DataFrame), "summarize_by_group with custom agg", "custom agg failed")
    s2 = utils.summarize_by_group(base, "site")
    show(isinstance(s2, pd.DataFrame), "summarize_by_group default (.describe())", "default agg failed")
except Exception as e:
    print(BAD, "summarize_by_group raised:", e)

print("\n Q3 checks complete.\n")
