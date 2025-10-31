import os, sys, traceback, random
from pathlib import Path

OK = ":)"; BAD = "x"
root = Path(".")
script = root/"q2_process_metadata.py"
config_file = root/"q2_config.txt"

print("\n🔍 Q2 checks...\n")

# ---------- A. Structural ----------
print("A) Structural")
print(OK,"q2_process_metadata.py exists" if script.exists() else BAD+" q2_process_metadata.py missing")
print(OK,"script is executable" if os.access(script, os.X_OK) else BAD+" script not executable (chmod +x q2_process_metadata.py)")

try:
    first = script.read_text(encoding="utf-8").splitlines()[0]
except Exception:
    first = ""
print(OK,"has python3 shebang" if first.startswith("#!/usr/bin/env python3") or first.startswith("#!/usr/bin/python3")
      else BAD+f" invalid/missing shebang: {first!r}")

has_main = False
try:
    has_main = "if __name__ == '__main__':" in script.read_text(encoding="utf-8")
except Exception: pass
print(OK,"has if __name__ == '__main__':" if has_main else BAD+" missing if __name__ == '__main__':")

# try executing the script (it should not crash)
try:
    import subprocess
    r = subprocess.run([sys.executable, str(script)], capture_output=True, text=True, timeout=60)
    print(OK,"script executes without errors" if r.returncode==0 else BAD+f" script exited with code {r.returncode}")
    if r.returncode!=0 and r.stderr:
        print("   └─ stderr:\n", r.stderr.strip()[:500])
except Exception as e:
    print(BAD,"error running script:", e)

# ---------- B. Function tests ----------
print("\nB) Function tests")
try:
    mod = __import__("q2_process_metadata")
except Exception as e:
    print(BAD,"import failed. Traceback:\n", "".join(traceback.format_exception_only(type(e), e)))
    sys.exit(0)

# 1) parse_config
try:
    parse_config = getattr(mod, "parse_config")
    # make a temp config if missing
    tmp_cfg = None
    if not config_file.exists():
        tmp_cfg = root/"_tmp_q2_config.txt"
        tmp_cfg.write_text("sample_data_rows=10\nsample_data_min=18\nsample_data_max=75\n", encoding="utf-8")
        use_cfg = tmp_cfg
    else:
        use_cfg = config_file
    cfg = parse_config(str(use_cfg))
    ok = isinstance(cfg, dict) and {'sample_data_rows','sample_data_min','sample_data_max'}.issubset(cfg.keys())
    print(OK,"parse_config returns required keys" if ok else BAD+" parse_config missing keys/invalid return")
finally:
    if 'tmp_cfg' in locals() and tmp_cfg and tmp_cfg.exists():
        tmp_cfg.unlink(missing_ok=True)

# 2) validate_config
try:
    validate_config = getattr(mod, "validate_config")
    v = validate_config({'sample_data_rows':'100','sample_data_min':'18','sample_data_max':'75'})
    ok = isinstance(v, dict) and v.get('sample_data_rows') and v.get('sample_data_min') and v.get('sample_data_max')
    print(OK,"validate_config passes typical values" if ok else BAD+" validate_config failed typical values")
except Exception as e:
    print(BAD,"validate_config raised:", e)

# 3) generate_sample_data
try:
    generate_sample_data = getattr(mod, "generate_sample_data")
    out = root/"_tmp_sample.csv"
    if out.exists(): out.unlink()
    generate_sample_data(str(out), {'sample_data_rows':'10','sample_data_min':'18','sample_data_max':'75'})
    ok_rows = out.exists() and len([l for l in out.read_text().splitlines() if l.strip()])==10
    ok_format = all(s.replace('.','',1).lstrip('-').isdigit() for s in out.read_text().splitlines() if s.strip())
    vals = [float(s) for s in out.read_text().splitlines() if s.strip()]
    ok_range = all(18<=x<=75 for x in vals) if vals else False
    print(OK,"generate_sample_data created correct file" if (ok_rows and ok_format and ok_range)
          else BAD+" sample file wrong rows/format/range")
    out.unlink(missing_ok=True)
except Exception as e:
    print(BAD,"generate_sample_data raised:", e)

# 4) calculate_statistics
try:
    calculate_statistics = getattr(mod, "calculate_statistics")
    stats = calculate_statistics([10,20,30,40,50])
    ok = isinstance(stats, dict) and abs(stats.get('mean',None)-30.0)<1e-9 and abs(stats.get('median',None)-30.0)<1e-9
    print(OK,"calculate_statistics mean/median correct" if ok else BAD+" calculate_statistics incorrect")
except Exception as e:
    print(BAD,"calculate_statistics raised:", e)

# ---------- C. Required outputs ----------
print("\nC) Required outputs")
print(OK,"data/sample_data.csv exists" if Path("data/sample_data.csv").exists() else BAD+" data/sample_data.csv missing")
print(OK,"output/statistics.txt exists" if Path("output/statistics.txt").exists() else BAD+" output/statistics.txt missing")
if Path("output/statistics.txt").exists():
    print(OK,"statistics.txt has content" if Path("output/statistics.txt").stat().st_size>0 else BAD+" statistics.txt empty")

print("\n Q2 checks complete.\n")
