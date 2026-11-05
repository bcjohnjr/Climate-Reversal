#!/usr/bin/env python3
"""Only check the independently reconstructed algebraic reference and leakage mass.

This is NOT a validation of full climate model outputs or ensemble metrics.
"""
import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def read(rel):
    with (ROOT/rel).open(encoding='utf8',newline='') as f:return list(csv.DictReader(f))

def num(s):return float(str(s).replace(',','').replace('−','-'))
ref={(round(num(r['total_gtco2']),2),int(num(r['rate_gtco2_per_year']))):num(r['late_minus_early_endpoint_ppm']) for r in read('science_figures/inputs/joos_linear_kernel_table_S3.csv')}
table=read('data/published_tables/Table_S3.csv')
assert len(ref)==len(table)==14
resids=[]
for row in table:
    key=(round(num(row['Total (GtCO₂)']),2),int(num(row['Rate (GtCO₂ yr⁻¹)'])))
    resids.append(abs(ref[key]-num(row['Linear kernel (ppm)'])))
assert max(resids)<.005, f'Linear reference residual > 0.005 ppm: {max(resids)}'
leaks={(num(r['leak_fraction']),int(num(r['leak_tau_years'])),r['phase']):num(r['total_leaked_gtco2']) for r in read('science_figures/inputs/leakage_accounting_table_S5.csv')}
reported=read('data/published_tables/Table_S5.csv')
assert len(reported)==7
leak_resids=[]
for row in reported:
    f=num(row['Leaking share (%)'])/100
    tau=0 if f==0 else int(num(row['e-folding time (yr)']))
    for phase in ['early','late']:
        leak_resids.append(abs(leaks[(f,tau,phase)]-num(row[f'Leaked by 2183, {phase} (GtCO₂)'])))
assert max(leak_resids)<.5,f'Leakage mass mismatch >0.5 GtCO2: {max(leak_resids)}'
print(f'PASS: 14 Joos predictions agree with Table S3 to 0.01 ppm (max deviation {max(resids):.6f} ppm).')
print(f'PASS: 14 leakage mass totals agree with Table S5 rounded to 1 GtCO2 (max deviation {max(leak_resids):.6f} GtCO2).')
print('Not checked: FaIR numerical outputs, ensemble statistics, figures, background scenarios.')
