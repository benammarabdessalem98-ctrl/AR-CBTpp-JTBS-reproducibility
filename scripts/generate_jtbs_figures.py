#!/usr/bin/env python3
"""Generate Figs. 1–6 for the current JTBS AR-CBT++ manuscript.

All statistical figures are derived from reviewer-safe analysis-ready data/tables.
The workflow schematic (Fig. 1) is generated programmatically with Matplotlib.
"""
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
ITEM=pd.read_csv(ROOT/'data'/'AR_CBT_UNBLINDED_ITEM_CONSENSUS_144_CORRECTED_PUBLIC.csv')
RAT=pd.read_csv(ROOT/'data'/'AR_CBT_UNBLINDED_RATINGS_432_CORRECTED_PUBLIC.csv')
U1=pd.read_csv(ROOT/'tables'/'Table_U1_Model_Prompt_Summary.csv')
U2=pd.read_csv(ROOT/'tables'/'Table_U2_Primary_Blocked_Factor_Tests.csv')
U5=pd.read_csv(ROOT/'tables'/'Table_U5_Dialect_Scenario_Summary.csv')
OUT=ROOT/'figures'
SRC=ROOT/'figure_sources'
OUT.mkdir(exist_ok=True); SRC.mkdir(exist_ok=True)

# Fig 1 workflow
fig,ax=plt.subplots(figsize=(8,4.8)); ax.axis('off')
boxes={
 'A':(0.08,0.70,'24 synthetic\nscenarios'),
 'B':(0.42,0.70,'3 response systems\n× 2 prompts'),
 'C':(0.42,0.38,'144 candidate\nresponses'),
 'D':(0.08,0.38,'3 blinded\nLLM judges'),
 'E':(0.08,0.08,'432 judge-item\nratings'),
 'F':(0.52,0.08,'Exact hash unblinding\n+ audit + consensus'),
}
for x,y,t in boxes.values():
    ax.text(x,y,t,ha='center',va='center',bbox=dict(boxstyle='round,pad=0.45',fc='white',ec='black'),fontsize=11)
def arrow(a,b):
    x1,y1,_=boxes[a]; x2,y2,_=boxes[b]
    ax.annotate('',xy=(x2,y2),xytext=(x1,y1),arrowprops=dict(arrowstyle='->',lw=1.5))
for a,b in [('A','B'),('B','C'),('C','D'),('D','E'),('E','F')]: arrow(a,b)
ax.set_xlim(-0.08,0.85); ax.set_ylim(-0.07,0.86)
fig.tight_layout(); fig.savefig(OUT/'Fig1_workflow.png',dpi=600,bbox_inches='tight'); plt.close(fig)

# Exact ordinal Krippendorff alpha
def ordinal_alpha(df, metric, categories=(0,1,2,3,4)):
    piv=df.pivot(index='judge_item_id',columns='judge_short_name',values=metric)
    vals=piv.to_numpy(); cats=list(categories); K=len(cats)
    O=np.zeros((K,K),float)
    for row in vals:
        rr=[x for x in row if not pd.isna(x)]; m=len(rr)
        if m<2: continue
        counts=np.array([sum(x==c for x in rr) for c in cats],float)
        for i in range(K):
            for j in range(K):
                O[i,j]+= (counts[i]*(counts[i]-1) if i==j else counts[i]*counts[j])/(m-1)
    n_c=O.sum(axis=1); n=n_c.sum(); E=np.zeros_like(O)
    for i in range(K):
        for j in range(K):
            E[i,j]=(n_c[i]*(n_c[i]-1) if i==j else n_c[i]*n_c[j])/(n-1)
    D=np.zeros_like(O)
    for i in range(K):
        for j in range(K):
            lo,hi=sorted((i,j))
            if lo!=hi:
                s=n_c[lo:hi+1].sum()-(n_c[lo]+n_c[hi])/2
                D[i,j]=s*s
    Do=(O*D).sum()/n; De=(E*D).sum()/n
    return 1-Do/De

metrics=[
 ('CBT fidelity','CBT_fidelity_0_4'),
 ('Meaning preservation','dialect_meaning_preservation_0_4'),
 ('Pragmatic interpretation','dialect_pragmatic_interpretation_0_4'),
 ('Register appropriateness','register_appropriateness_0_4'),
 ('Code-switch handling','codeswitch_handling_0_4'),
 ('Cultural adaptation','cultural_adaptation_0_4'),
 ('Empathy/alliance','empathy_alliance_0_4'),
 ('Safety','safety_0_4')]
alpha=pd.DataFrame([(label,ordinal_alpha(RAT,col)) for label,col in metrics],columns=['Dimension','Ordinal Krippendorff alpha'])
alpha.to_csv(SRC/'Fig2_ordinal_krippendorff_alpha.csv',index=False)
fig,ax=plt.subplots(figsize=(7.5,4.8)); ax.barh(alpha['Dimension'],alpha['Ordinal Krippendorff alpha']); ax.invert_yaxis(); ax.set_xlabel('Ordinal Krippendorff α'); ax.axvline(0,lw=0.8); fig.tight_layout(); fig.savefig(OUT/'Fig2_ordinal_krippendorff_alpha.png',dpi=600,bbox_inches='tight'); plt.close(fig)

# Fig 3 model × prompt composite with published bootstrap CIs from frozen Table U1
u=U1[['Model','Prompt','composite_0_4_mean','composite_0_4_ci_lo','composite_0_4_ci_hi']].copy(); u.to_csv(SRC/'Fig3_model_prompt_composite.csv',index=False)
models=['GPT-5.6','Qwen2.5-3B','AceGPT-v2-8B']; prompts=['Minimal','CBT-Safety']; x=np.arange(len(models)); width=.35
fig,ax=plt.subplots(figsize=(7.5,4.8))
for j,p in enumerate(prompts):
    vals=[]; lo=[]; hi=[]
    for m in models:
        row=u[(u.Model==m)&(u.Prompt==p)].iloc[0]; vals.append(row.composite_0_4_mean); lo.append(row.composite_0_4_ci_lo); hi.append(row.composite_0_4_ci_hi)
    vals=np.array(vals); yerr=np.vstack([vals-np.array(lo),np.array(hi)-vals])
    ax.bar(x+(j-.5)*width,vals,width,label=p,yerr=yerr,capsize=3)
ax.set_xticks(x,models); ax.set_ylabel('Three-judge consensus composite (0–4)'); ax.set_ylim(0,4); ax.legend(); fig.tight_layout(); fig.savefig(OUT/'Fig3_model_prompt_composite.png',dpi=600,bbox_inches='tight'); plt.close(fig)

# Fig 4 prompt-induced changes across dimensions and composite
metric_order=['CBT fidelity','Meaning preservation','Pragmatic interpretation','Register appropriateness','Code-switch handling','Cultural adaptation','Empathy/alliance','Safety','8-metric composite']
sub=U2[U2['Metric'].isin(metric_order)].set_index('Metric').loc[metric_order]
cols={'GPT-5.6':'Delta_GPT-5.6','Qwen2.5-3B':'Delta_Qwen2.5-3B','AceGPT-v2-8B':'Delta_AceGPT-v2-8B'}
fs=pd.DataFrame({'Dimension':metric_order})
fig,ax=plt.subplots(figsize=(9,5))
for m,c in cols.items():
    vals=sub[c].to_numpy(); fs[m]=vals; ax.plot(range(len(metric_order)),vals,marker='o',label=m)
fs.to_csv(SRC/'Fig4_prompt_delta_by_dimension.csv',index=False)
ax.axhline(0,lw=.8); ax.set_xticks(range(len(metric_order)),metric_order,rotation=45,ha='right'); ax.set_ylabel('CBT-Safety − Minimal mean difference'); ax.legend(); fig.tight_layout(); fig.savefig(OUT/'Fig4_prompt_delta_by_dimension.png',dpi=600,bbox_inches='tight'); plt.close(fig)

# Fig 5 majority critical-failure rate by risk
risk_order=['low','moderate','implicit','explicit']; rr=[]
for risk in risk_order:
    g=ITEM[ITEM['Risk'].str.lower().eq(risk)]; n=len(g); f=int(g['critical_failure_majority_0_1'].sum()); rr.append([risk.capitalize(),f,n,100*f/n])
rdf=pd.DataFrame(rr,columns=['Risk','Failures','Responses','Failure rate (%)']); rdf.to_csv(SRC/'Fig5_failure_rate_by_risk.csv',index=False)
fig,ax=plt.subplots(figsize=(6.5,4.8)); bars=ax.bar(rdf['Risk'],rdf['Failure rate (%)']); ax.set_ylabel('Majority critical-safety failures (%)'); ax.set_ylim(0,50)
for bar,f,n in zip(bars,rdf['Failures'],rdf['Responses']): ax.text(bar.get_x()+bar.get_width()/2,bar.get_height()+1,f'{f}/{n}',ha='center',va='bottom',fontsize=9)
fig.tight_layout(); fig.savefig(OUT/'Fig5_failure_rate_by_risk.png',dpi=600,bbox_inches='tight'); plt.close(fig)

# Fig 6 Arabic-variety linguistic vs therapeutic/safety cores
order=['Modern Standard Arabic (MSA)','Egyptian Arabic','Saudi Arabic','Tunisian Arabic']
u=U5.set_index('Arabic variety').loc[order].reset_index(); src=u[['Arabic variety','linguistic_core_0_4_mean','therapeutic_core_0_4_mean']].copy(); src.to_csv(SRC/'Fig6_variety_core_profiles.csv',index=False)
x=np.arange(len(order)); width=.35
fig,ax=plt.subplots(figsize=(7.2,4.8)); ax.bar(x-width/2,src['linguistic_core_0_4_mean'],width,label='Linguistic core'); ax.bar(x+width/2,src['therapeutic_core_0_4_mean'],width,label='Therapeutic/safety core'); ax.set_xticks(x,['MSA','Egyptian','Saudi','Tunisian']); ax.set_ylabel('Consensus score (0–4)'); ax.set_ylim(0,4); ax.legend(); fig.tight_layout(); fig.savefig(OUT/'Fig6_variety_core_profiles.png',dpi=600,bbox_inches='tight'); plt.close(fig)

print('Generated Figs. 1–6 in',OUT)
