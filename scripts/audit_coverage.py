"""A1 phase 2-3: candidates and coverage against both existing catalogues."""
import pandas as pd, glob, os
R="results/audit"
inv=pd.concat([pd.read_csv(f, low_memory=False) for f in glob.glob(f"{R}/inventory_*.csv")], ignore_index=True)
c1=pd.read_csv("docs/catalog/catalog.csv", low_memory=False); c2=pd.read_csv("docs/catalog_agy/catalog.csv", low_memory=False)
def paths(df):
    col=[c for c in df.columns if c.lower() in ("path","file","filepath","abs_path")][0]
    return col, df[col].astype(str)
k1,p1=paths(c1); k2,p2=paths(c2)
print("catalog cols:", k1, k2)
cat1=set(p1); cat2=set(p2)
inv["cand"]=inv.candidate==1
print("roots:", inv.groupby("root").size().to_dict()); print("candidates by root:", inv[inv.cand].groupby("root").size().to_dict(), "total", int(inv.cand.sum()), "of", len(inv))
# agy paths are relative to /mnt/phd_data/phd_master/ and tree-relative; match on suffix
def covered(p):
    if p in cat1: return "scan"
    if any(p.endswith(x) for x in ()): return ""
    return ""
suffix2=set(os.path.basename(x) for x in cat2); suffix1=set(os.path.basename(x) for x in cat1)
inv["in_scan"]=inv.path.isin(cat1)
inv["in_agy_exact"]=inv.path.isin(cat2) | inv.path.str.replace("/mnt/phd_data/phd_master/","",regex=False).isin(cat2)
cand=inv[inv.cand].copy()
cand["base"]=cand.path.map(os.path.basename)
cand["covered_exact"]=cand.in_scan|cand.in_agy_exact
cand["covered_by_name"]=cand.base.isin(suffix1|suffix2)
print("candidates exact-covered:", int(cand.covered_exact.sum()), "| name-covered (weaker):", int(cand.covered_by_name.sum()), "| neither:", int((~cand.covered_by_name).sum()))
cand["top"]=cand.path.str.split("/").str[:6].str.join("/")
un=cand[~cand.covered_by_name]
un.to_csv(f"{R}/uncovered_candidates.csv", index=False); cand.to_csv(f"{R}/candidates.csv", index=False)
print(un.groupby("root").size().to_dict())
print(un.groupby("top").size().sort_values(ascending=False).head(30).to_string())
