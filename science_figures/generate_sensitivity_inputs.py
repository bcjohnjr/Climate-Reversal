#!/usr/bin/env python3
"""Derive disclosed sensitivity INPUT trajectories; this does not rerun FaIR.

V67 fixed-source reference from recovered GitHub Actions file; formulas and
schedule parameters from submitted GBC Supporting Information. 2026-2183 rows.
"""
import csv, math
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/'data/v67/cases/fixed__early/trajectories/fixed__early.csv'
OUT = ROOT/'science_figures/inputs'
COLS = ('year','gross_co2_gtco2','permafrost_co2_gtco2','stored_carbon_reversal_gtco2','cdr_gtco2','net_co2_gtco2')
TOTAL = 2013.8807318595145

def load(path):
    with path.open(encoding='utf8',newline='') as f:
        return [{k:float(v) for k,v in row.items()} for row in csv.DictReader(f)]

def save(path,rows,cols):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',encoding='utf8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=cols);w.writeheader();w.writerows(rows)
base=load(BASE)
assert len(base)==158 and [int(r['year']) for r in base]==list(range(2026,2184))
years=[int(r['year']) for r in base]

def schedule(total,rate,late):
    full=int(total//rate);remain=total-full*rate
    if abs(remain)<1e-10: remain=0.
    n=full+bool(remain)
    candidates=list(range(1,len(years)))
    assert n<=len(candidates)
    ix=candidates[-n:] if late else candidates[:n]
    a=[0.]*len(years)
    if late:
        if remain: a[ix[0]]=remain;ix=ix[1:]
        for i in ix:a[i]=rate
    else:
        for i in ix[:full]:a[i]=rate
        if remain:a[ix[full]]=remain
    assert abs(sum(a)-total)<1e-7
    return a

def scenario(cdr,source=None):
    source=source if source is not None else [r['stored_carbon_reversal_gtco2'] for r in base]
    result=[]
    for i,r in enumerate(base):
        gross=r['gross_co2_gtco2'];pf=r['permafrost_co2_gtco2'];rev=source[i]
        result.append(dict(year=int(r['year']),gross_co2_gtco2=gross,permafrost_co2_gtco2=pf,stored_carbon_reversal_gtco2=rev,cdr_gtco2=cdr[i],net_co2_gtco2=gross+pf+rev-cdr[i]))
    return result

def joos(t):
    return .2173+.2240*math.exp(-t/394.4)+.2824*math.exp(-t/36.54)+.2763*math.exp(-t/4.304)

manifest=[];linear=[]
for total in [100,250,500,1000,TOTAL]:
    for rate in [2,5,10,20]:
        if total/rate>157+1e-8: continue
        tag=f'cdr_{total:.2f}_rate_{rate}'
        e=schedule(total,rate,False);l=schedule(total,rate,True)
        for phase,arr in [('early',e),('late',l)]:
            path=OUT/'size_rate'/f'{tag}_{phase}.csv';save(path,scenario(arr),COLS)
            manifest.append(dict(file=str(path.relative_to(ROOT)),group='size_rate',total_gtco2=total,rate_gtco2_per_year=rate,phase=phase,leak_fraction='',leak_tau='',off_stored_reversal_zero='false'))
        linear.append(dict(total_gtco2=total,rate_gtco2_per_year=rate,late_minus_early_endpoint_ppm=sum((l[i]-e[i])*joos(2183-y) for i,y in enumerate(years))/7.8))
assert len(linear)==14
save(OUT/'joos_linear_kernel_table_S3.csv',linear,list(linear[0]))

leaks=[]
for frac in [0.,.1,.25,.5]:
    for tau in ([0] if frac==0 else [20,100]):
        for phase in ['early','late']:
            cdr=schedule(TOTAL,20,phase=='late');stock=0.;released=[]
            for r in cdr:
                leak=stock*(-math.expm1(-1./tau)) if tau else 0.
                stock=stock-leak+frac*r
                released.append(leak)
            path=OUT/'leakage'/f'leak_{frac:.2f}_tau_{tau}_{phase}.csv'
            save(path,scenario(cdr,released),COLS)
            manifest.append(dict(file=str(path.relative_to(ROOT)),group='leakage',total_gtco2=TOTAL,rate_gtco2_per_year=20,phase=phase,leak_fraction=frac,leak_tau=tau,off_stored_reversal_zero='true'))
            leaks.append(dict(leak_fraction=frac,leak_tau_years=tau,phase=phase,total_leaked_gtco2=sum(released),store_remaining_gtco2=stock))
save(OUT/'leakage_accounting_table_S5.csv',leaks,list(leaks[0]))
assert round(next(x for x in leaks if x['leak_fraction']==.5 and x['leak_tau_years']==20 and x['phase']=='early')['total_leaked_gtco2'])==995
assert round(next(x for x in leaks if x['leak_fraction']==.5 and x['leak_tau_years']==20 and x['phase']=='late')['total_leaked_gtco2'])==803

front=[];back=[]
for y in years:
    if y<2030:front.append(0.);back.append(0.)
    else:
        front.append((.91+(10-.91)*(y-2030)/10) if y<=2040 else (10. if y<=2074 else 0.))
        back.append((.16+(11.1-.16)*(y-2030)/70) if y<=2100 else 0.)
for tag,values in [('front_loaded',front),('back_loaded',back)]:
    # Published initial and final rates are rounded; scale their linear shapes
    # by one common factor to satisfy exactly 400 GtCO2 in the 2030-2100 window.
    adjusted=[r*(400./sum(values)) for r in values]
    assert abs(sum(adjusted)-400)<1e-7
    path=OUT/'pathways_2100'/f'{tag}_400gt.csv'
    save(path,scenario(adjusted),COLS)
    manifest.append(dict(file=str(path.relative_to(ROOT)),group='pathways_2100',total_gtco2=400,rate_gtco2_per_year=max(adjusted),phase=tag,leak_fraction='',leak_tau='',off_stored_reversal_zero='false'))
save(OUT/'reconstructed_inputs_manifest.csv',manifest,list(manifest[0]))
print(f'Created {len(manifest)} input trajectories and {len(linear)} Joos linear predictions; not FaIR model outputs.')
