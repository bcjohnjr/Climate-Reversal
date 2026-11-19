#!/usr/bin/env python3
"""Reconstruct corrected Fig. 2 from *archived* 841-member FaIR outputs.

Run in the bcjohnjr/Climate-Reversal repository root:
    pip install numpy pandas matplotlib pillow
    python FAIR_REBUILD_FIG2.py

Inputs required at repository root:
    FAIR_56_CASE_OUTPUTS.zip
    V67_COUPLED_BOUND2183_EARLY.zip
    V67_COUPLED_BOUND2183_LATE.zip

The programme-coupled V67 outputs are at FaIR bound 2183; fixed-source and
ideal-permanence FaIR sensitivity outputs are at bound 2184. This does NOT
simulate the missing programme-coupled bound-2184 case.
"""
from pathlib import Path
import zipfile, io, json
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

V6=zipfile.ZipFile('FAIR_56_CASE_OUTPUTS.zip')

def v6_df(case,metric):
    return pd.read_csv(io.BytesIO(V6.read(f'results/{case}/{metric}.csv')))

def v67_df(case,phase,metric):
    assert case=='coupled'
    p=Path(f'V67_COUPLED_BOUND2183_{phase.upper()}.zip')
    with zipfile.ZipFile(p) as z:
        return pd.read_csv(io.BytesIO(z.read(f'fair_work/{metric}.csv')))

record={}
for case,labels in [('Fixed source',('size_2013.88_rate_20_early','size_2013.88_rate_20_late')),('Ideal permanence',('leak_0.00_tau_0_early','leak_0.00_tau_0_late')),('Programme-coupled',(None,None))]:
 if labels[0] is None:
  e=v67_df('coupled','early','fair_member_metrics');l=v67_df('coupled','late','fair_member_metrics');bound=2183
 else:
  e=v6_df(labels[0],'fair_member_metrics_end_2183');l=v6_df(labels[1],'fair_member_metrics_end_2183');bound=2184
 ea=e.set_index('member_id').sort_index();la=l.set_index('member_id').sort_index()
 assert len(ea)==len(la)==841 and ea.index.equals(la.index)
 m={
  'forcing':(ea['integrated_co2_forcing_benefit_wm2_year']-la['integrated_co2_forcing_benefit_wm2_year']).to_numpy(),
  'co2':(la['terminal_delta_co2_ppm']-ea['terminal_delta_co2_ppm']).to_numpy(),
  'warming':(ea['integrated_avoided_warming_c_year']-la['integrated_avoided_warming_c_year']).to_numpy(),
 }
 assert all(np.isfinite(v).all() and len(v)==841 for v in m.values())
 record[case]={**m,'bound':bound,'min':{k:float(v.min()) for k,v in m.items()},'p05':{k:float(np.quantile(v,.05)) for k,v in m.items()},'p50':{k:float(np.median(v)) for k,v in m.items()},'p95':{k:float(np.quantile(v,.95)) for k,v in m.items()}}
print('FIGURE2_RECHECK',json.dumps({k:dict(bound=v['bound'],min=v['min'],p50=v['p50']) for k,v in record.items()},indent=2))
assert round(record['Programme-coupled']['min']['forcing'],2)==58.35
assert round(record['Programme-coupled']['min']['co2'],2)==15.93
assert round(record['Programme-coupled']['min']['warming'],2)==22.93

# Recreate Fig 2 directly from deposited 841 member values. Central markers use Table 1 values (differences of median series).
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8,'axes.labelsize':8,'xtick.labelsize':8,'ytick.labelsize':8,'legend.fontsize':7})
fig,axes=plt.subplots(1,3,figsize=(11.5,4.0),dpi=300, gridspec_kw={'wspace':.34})
cs=['Fixed\nsource','Ideal\npermanence','Programme-\ncoupled'];ks=list(record)
central={'forcing':[78.70,78.75,75.74],'co2':[20.40,20.40,18.61],'warming':[45.52,45.56,43.64]}
hector={'forcing':[61.97,61.95,59.36],'co2':[29.90,29.72,28.63],'warming':[45.61,45.61,43.70]}
oscar={'forcing':[84.68,83.83,79.39],'co2':[23.69,22.14,23.13]}
oscar_min={'forcing':[4.45,15.20,6.27],'co2':[-32.37,-32.20,-42.85]}
colors={'fair':'#2d77c7','hector':'#e36e32','oscar':'#16a777'}
for j,(key,lab,ylims) in enumerate([
 ('forcing','Early − late integrated\nCO₂-forcing benefit (W m⁻² yr)',(-5,112)),
 ('co2','Late − early terminal\nCO₂ benefit (ppm)',(-52,43)),
 ('warming','Early − late integrated\navoided warming (°C yr)',(0,85)),
]):
 ax=axes[j];data=[record[k][key] for k in ks];parts=ax.violinplot(data,positions=[1,2,3],widths=.47,showmeans=False,showmedians=False,showextrema=False,bw_method=.24)
 for body in parts['bodies']:
  body.set_facecolor(colors['fair']);body.set_edgecolor('none');body.set_alpha(.26)
 for i,k in enumerate(ks):
  ax.vlines(i+1,record[k]['p05'][key],record[k]['p95'][key],color=colors['fair'],linewidth=2,zorder=3)
  ax.scatter(i+1,central[key][i],color=colors['fair'],s=32,zorder=5)
  ax.scatter(i+.77,hector[key][i],marker='s',color=colors['hector'],s=31,zorder=5)
  if key in oscar:
   ax.scatter(i+1.24,oscar[key][i],marker='D',color=colors['oscar'],s=31,zorder=5)
   ax.scatter(i+1.24,oscar_min[key][i],marker='D',facecolors='white',edgecolors=colors['oscar'],linewidth=1.4,s=31,zorder=5)
   if key=='co2': ax.annotate(['82.5%','82.5%','80.0%'][i],(i+1.24,oscar_min[key][i]),xytext=(0,-11),textcoords='offset points',ha='center',fontsize=7)
 ax.set_xlim(.42,3.61);ax.set_ylim(*ylims);ax.set_xticks([1,2,3],cs);ax.set_ylabel(lab)
 ax.grid(axis='y',alpha=.2,zorder=0);ax.set_axisbelow(True);ax.spines['top'].set_visible(False);ax.spines['right'].set_visible(False)
 ax.text(.01,.98,'ABC'[j],transform=ax.transAxes,va='top',ha='left',fontsize=12,fontweight='bold')
 if key=='co2':ax.axhline(0,color='#666',lw=.8)
from matplotlib.lines import Line2D
fig.legend(handles=[Line2D([0],[0],color=colors['fair'],lw=6,alpha=.35,label='FaIR paired members (841)'),Line2D([0],[0],color=colors['fair'],marker='o',lw=1,label='FaIR central; 5–95%'),Line2D([0],[0],color=colors['hector'],marker='s',lw=0,label='Hector'),Line2D([0],[0],color=colors['oscar'],marker='D',lw=0,label='OSCAR median'),Line2D([0],[0],color=colors['oscar'],marker='D',markerfacecolor='white',lw=0,label='OSCAR least favourable')],loc='upper center',bbox_to_anchor=(.5,1.0),ncol=5,frameon=False,fontsize=7)
fig.subplots_adjust(left=.075,right=.986,top=.87,bottom=.19)
fig.text(.51,.065,'FaIR: bound 2184 (fixed and ideal); archived bound 2183 (programme-coupled)',ha='center',fontsize=7.3,color='#4d5661')
figp=Path('FAIR_FIG2_RECONSTRUCTED.tif');fig.savefig(figp,dpi=600,format='tiff',pil_kwargs={'compression':'tiff_lzw'});plt.close(fig)

# Save reproducible statistics for the three paired protocols.
rows=[]
for name,item in record.items():
    rows.append({'protocol':name,'fair_bound':item['bound'],
        **{f'min_{k}':v for k,v in item['min'].items()},
        **{f'median_paired_{k}':v for k,v in item['p50'].items()},
        **{f'p05_{k}':v for k,v in item['p05'].items()},
        **{f'p95_{k}':v for k,v in item['p95'].items()}})
pd.DataFrame(rows).to_csv('FAIR_FIG2_PAIRED_AUDIT.csv',index=False)
print('Recreated',figp,figp.stat().st_size,'bytes and FAIR_FIG2_PAIRED_AUDIT.csv')
