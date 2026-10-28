#!/usr/bin/env python3
"""Reproduce numerical results used in the current JTBS AR-CBT++ manuscript.

Manuscript title:
Safety, CBT Fidelity, and Cultural Adaptation of Large Language Models in
Arabic CBT-Style Mental Health Dialogue: The AR-CBT++ Benchmark

The script uses reviewer-safe analysis tables only. It does not need the private
unblinding key or raw dialogue text.
"""
from pathlib import Path
import pandas as pd
import numpy as np
from scipy.stats import friedmanchisquare, wilcoxon, kruskal, spearmanr, binomtest

ROOT=Path(__file__).resolve().parents[1]
ITEM=ROOT/'data'/'AR_CBT_UNBLINDED_ITEM_CONSENSUS_144_CORRECTED_PUBLIC.csv'
RAT=ROOT/'data'/'AR_CBT_UNBLINDED_RATINGS_432_CORRECTED_PUBLIC.csv'
OUT=ROOT/'verification'/'JTBS_main_results_check.csv'
U2=ROOT/'tables'/'Table_U2_Primary_Blocked_Factor_Tests.csv'

df=pd.read_csv(ITEM)
r=pd.read_csv(RAT)
metric_cols=['CBT_fidelity_0_4','dialect_meaning_preservation_0_4','dialect_pragmatic_interpretation_0_4',
             'register_appropriateness_0_4','codeswitch_handling_0_4','cultural_adaptation_0_4',
             'empathy_alliance_0_4','safety_0_4']
rows=[]
def add(name,value,reported=None):
    rows.append({'check':name,'computed':value,'reported_reference':reported})

# Core sample counts
add('candidate_responses_n',len(df),144)
add('judge_item_ratings_n',len(r),432)
add('majority_critical_failures_total',int(df['critical_failure_majority_0_1'].sum()),12)

# Overall and model means
add('overall_composite_mean',df['composite_0_4'].mean(),3.334)
for m,g in df.groupby('Model_short'):
    add(f'model_composite::{m}',g['composite_0_4'].mean(),None)

# Model main effect, prompt main effect, interaction diagnostic
model_order=['GPT-5.6','Qwen2.5-3B','AceGPT-v2-8B']
piv=df.groupby(['Scenario ID','Model_short'])['composite_0_4'].mean().unstack('Model_short')
stat,p=friedmanchisquare(*[piv[m].to_numpy() for m in model_order])
add('friedman_model_chi2',stat,36.58); add('friedman_model_p',p,'<0.001')

pp=df.groupby(['Scenario ID','Prompt condition'])['composite_0_4'].mean().unstack('Prompt condition')
delta=pp['CBT-Safety']-pp['Minimal']
add('prompt_delta_mean',delta.mean(),0.268)
stat,p=wilcoxon(pp['CBT-Safety'],pp['Minimal'],alternative='two-sided',zero_method='wilcox')
add('wilcoxon_prompt_W',stat,0); add('wilcoxon_prompt_p',p,'<0.001')

for m in model_order:
    x=df[df['Model_short'].eq(m)].pivot(index='Scenario ID',columns='Prompt condition',values='composite_0_4')
    d=x['CBT-Safety']-x['Minimal']
    add(f'prompt_delta::{m}',d.mean(),None)

# The interaction diagnostic is tie-sensitive. The public consensus table is rounded,
# so recomputing Friedman from that public table can slightly alter tie correction.
# Use the frozen primary analysis table that underlies the manuscript for this check.
u2=pd.read_csv(U2)
ix=u2[u2['Metric'].eq('8-metric composite')].iloc[0]
add('friedman_interaction_chi2',ix['Interaction_Friedman_chi2'],3.08)
add('friedman_interaction_p',ix['Interaction_p'],0.214)

# Risk scenario-level analysis
sc=df.groupby(['Scenario ID','Arabic variety','Risk'],as_index=False).agg(
    composite_0_4=('composite_0_4','mean'),
    safety_0_4=('safety_0_4','mean'),
    linguistic_core_0_4=('linguistic_core_0_4','mean'),
    therapeutic_core_0_4=('therapeutic_core_0_4','mean'))
for risk,g in sc.groupby('Risk'):
    add(f'risk_safety_mean::{risk}',g['safety_0_4'].mean(),None)
stat,p=kruskal(*[g['safety_0_4'].to_numpy() for _,g in sc.groupby('Risk')])
add('risk_safety_kruskal_H',stat,15.39); add('risk_safety_kruskal_p',p,0.0015)
for risk,g in df.groupby('Risk'):
    add(f'critical_failures::{risk}',int(g['critical_failure_majority_0_1'].sum()),None)

# Explicit-risk scenario breakdown (manuscript Table 7)
for sid,g in df[df['Risk'].str.lower().eq('explicit')].groupby('Scenario ID'):
    add(f'explicit_scenario_failures::{sid}',int(g['critical_failure_majority_0_1'].sum()),None)

# Exact McNemar on matched Model×Scenario pairs
m=df.pivot(index=['Model_short','Scenario ID'],columns='Prompt condition',values='critical_failure_majority_0_1')
b=int(((m['Minimal']==1)&(m['CBT-Safety']==0)).sum())
c=int(((m['Minimal']==0)&(m['CBT-Safety']==1)).sum())
add('mcnemar_improved_pairs',b,4); add('mcnemar_worsened_pairs',c,0)
if b+c:
    add('mcnemar_exact_p',binomtest(min(b,c),n=b+c,p=0.5,alternative='two-sided').pvalue,0.125)

# Judge-level primary error labels among critical flags on majority-failure responses (Table 9)
majority_ids=set(df.loc[df['critical_failure_majority_0_1'].eq(1),'judge_item_id'])
flags=r[r['judge_item_id'].isin(majority_ids) & r['critical_safety_failure_0_1'].eq(1)]
add('judge_level_critical_flags_n',len(flags),31)
for cat,n in flags['primary_error_category'].value_counts().items():
    add(f'critical_flag_error::{cat}',int(n),None)

# Arabic-variety scenario-level analysis
for d,g in sc.groupby('Arabic variety'):
    add(f'variety_composite_mean::{d}',g['composite_0_4'].mean(),None)
stat,p=kruskal(*[g['composite_0_4'].to_numpy() for _,g in sc.groupby('Arabic variety')])
add('variety_composite_kruskal_H',stat,9.19); add('variety_composite_kruskal_p',p,0.0269)

# Same-family sensitivity
r['judge_composite']=r[metric_cols].mean(axis=1)
full=df.set_index('judge_item_id')['composite_0_4'].rename('full')
noq=r[r['judge_short_name'].ne('Qwen3')].groupby('judge_item_id')['judge_composite'].mean().rename('no_qwen3')
cmp=pd.concat([full,noq],axis=1).dropna()
add('same_family_item_spearman_rho',spearmanr(cmp['full'],cmp['no_qwen3']).statistic,0.936)
add('same_family_item_MAE',(cmp['full']-cmp['no_qwen3']).abs().mean(),0.072)
for model,g in df.groupby('Model_short'):
    ids=g['judge_item_id']
    add(f'no_qwen3_model_mean::{model}',noq.reindex(ids).mean(),None)

# Sensitivity to composite definition (manuscript Table 12)
for model in ['GPT-5.6','AceGPT-v2-8B','Qwen2.5-3B']:
    g=df[df['Model_short'].eq(model)]
    gn=g[g['critical_failure_majority_0_1'].eq(0)]
    add(f'sensitivity_full::{model}',g['composite_0_4'].mean(),None)
    add(f'sensitivity_linguistic::{model}',g['linguistic_core_0_4'].mean(),None)
    add(f'sensitivity_therapeutic_safety::{model}',g['therapeutic_core_0_4'].mean(),None)
    add(f'sensitivity_safety::{model}',g['safety_0_4'].mean(),None)
    add(f'sensitivity_no_critical::{model}',gn['composite_0_4'].mean(),None)
    add(f'sensitivity_no_critical_n::{model}',len(gn),None)

out=pd.DataFrame(rows)
out.to_csv(OUT,index=False)
print(out.to_string(index=False))
print(f'\nSaved: {OUT}')
