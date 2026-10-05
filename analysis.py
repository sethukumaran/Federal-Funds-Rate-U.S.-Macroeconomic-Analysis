# Federal Funds & U.S. Macroeconomic Indicators Analysis
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

INPUT = Path('index.csv')
OUT = Path('outputs')
OUT.mkdir(exist_ok=True)

# -------------------- Load & validate --------------------
df = pd.read_csv(INPUT)
df.columns = [c.strip() for c in df.columns]
df['Date'] = pd.to_datetime(dict(year=df['Year'], month=df['Month'], day=df['Day']), errors='coerce')
df = df.sort_values('Date').reset_index(drop=True)

print('Shape:', df.shape)
print('\nData types:\n', df.dtypes)
print('\nMissing values:\n', df.isna().sum())
print('\nDuplicate rows:', df.duplicated().sum())
print('\nSummary:\n', df.describe(include='all').T)

# Basic data-quality checks
assert df['Date'].notna().all(), 'Invalid dates found'
assert df.duplicated().sum() == 0, 'Duplicate rows found'

# Derived fields
df['Quarter'] = df['Date'].dt.to_period('Q').astype(str)
df['Decade'] = (df['Year'] // 10) * 10
df['Effective_Rate_Change'] = df['Effective Federal Funds Rate'].diff()
df['Real_Rate_Proxy'] = df['Effective Federal Funds Rate'] - df['Inflation Rate']
df['Inflation_Regime'] = pd.cut(
    df['Inflation Rate'], [-np.inf, 2, 4, 6, np.inf],
    labels=['<2%', '2-4%', '4-6%', '>=6%']
)
df['Unemployment_Regime'] = pd.cut(
    df['Unemployment Rate'], [-np.inf, 5, 7, 9, np.inf],
    labels=['<5%', '5-7%', '7-9%', '>=9%']
)

# Save cleaned/feature-engineered data
df.to_csv(OUT / 'cleaned_fed_macro_data.csv', index=False)

# -------------------- KPI / business metrics --------------------
kpis = {
    'rows': len(df),
    'date_start': str(df['Date'].min().date()),
    'date_end': str(df['Date'].max().date()),
    'effective_rate_max': float(df['Effective Federal Funds Rate'].max()),
    'effective_rate_min': float(df['Effective Federal Funds Rate'].min()),
    'inflation_max': float(df['Inflation Rate'].max()),
    'unemployment_max': float(df['Unemployment Rate'].max()),
    'gdp_min': float(df['Real GDP (Percent Change)'].min()),
    'gdp_max': float(df['Real GDP (Percent Change)'].max()),
}
print('\nKPIs:', kpis)

# Annual view
annual = df.groupby('Year').agg(
    avg_effective_rate=('Effective Federal Funds Rate','mean'),
    avg_inflation=('Inflation Rate','mean'),
    avg_unemployment=('Unemployment Rate','mean'),
    avg_gdp_growth=('Real GDP (Percent Change)','mean'),
    max_effective_rate=('Effective Federal Funds Rate','max'),
    min_effective_rate=('Effective Federal Funds Rate','min'),
    observations=('Date','count')
).reset_index()
annual.to_csv(OUT / 'annual_summary.csv', index=False)

# Decade view
decade = df.groupby('Decade').agg(
    avg_effective_rate=('Effective Federal Funds Rate','mean'),
    avg_inflation=('Inflation Rate','mean'),
    avg_unemployment=('Unemployment Rate','mean'),
    avg_gdp_growth=('Real GDP (Percent Change)','mean'),
    peak_effective_rate=('Effective Federal Funds Rate','max'),
    peak_inflation=('Inflation Rate','max')
).reset_index()
decade.to_csv(OUT / 'decade_summary.csv', index=False)

# Correlation matrix using pairwise complete observations
num_cols = ['Federal Funds Target Rate','Effective Federal Funds Rate',
            'Real GDP (Percent Change)','Unemployment Rate','Inflation Rate']
corr = df[num_cols].corr()
corr.to_csv(OUT / 'correlation_matrix.csv')

# High-stress observations
stress = df[
    (df['Inflation Rate'] >= 6) |
    (df['Unemployment Rate'] >= 8) |
    (df['Real GDP (Percent Change)'] < 0)
].copy()
stress.to_csv(OUT / 'macro_stress_periods.csv', index=False)

# -------------------- Visualizations --------------------
def savefig(name):
    plt.tight_layout()
    plt.savefig(OUT / name, dpi=160, bbox_inches='tight')
    plt.close()

# 1. Policy rate over time
plt.figure(figsize=(12,5))
plt.plot(df['Date'], df['Effective Federal Funds Rate'], linewidth=1.5)
plt.title('Effective Federal Funds Rate Over Time')
plt.xlabel('Date'); plt.ylabel('Rate (%)'); plt.grid(alpha=.25)
savefig('01_effective_fed_funds_rate.png')

# 2. Inflation and policy rate
fig, ax = plt.subplots(figsize=(12,5))
ax.plot(df['Date'], df['Inflation Rate'], label='Inflation Rate')
ax.plot(df['Date'], df['Effective Federal Funds Rate'], label='Effective Fed Funds Rate', alpha=.8)
ax.set_title('Inflation vs. Federal Funds Rate')
ax.set_xlabel('Date'); ax.set_ylabel('Rate (%)'); ax.grid(alpha=.25); ax.legend()
savefig('02_inflation_vs_policy.png')

# 3. Unemployment
plt.figure(figsize=(12,5))
plt.plot(df['Date'], df['Unemployment Rate'], linewidth=1.4)
plt.title('Unemployment Rate Over Time')
plt.xlabel('Date'); plt.ylabel('Unemployment (%)'); plt.grid(alpha=.25)
savefig('03_unemployment.png')

# 4. GDP growth
plt.figure(figsize=(12,5))
plt.plot(df['Date'], df['Real GDP (Percent Change)'], marker='o', markersize=2, linewidth=.9)
plt.axhline(0, linewidth=1)
plt.title('Real GDP Growth Observations')
plt.xlabel('Date'); plt.ylabel('GDP Growth (%)'); plt.grid(alpha=.25)
savefig('04_gdp_growth.png')

# 5. Decade comparison
plot_dec = decade.dropna(subset=['avg_inflation','avg_unemployment','avg_effective_rate'])
fig, ax = plt.subplots(figsize=(11,5))
x = np.arange(len(plot_dec))
w = .25
ax.bar(x-w, plot_dec['avg_effective_rate'], width=w, label='Avg Fed Funds Rate')
ax.bar(x, plot_dec['avg_inflation'], width=w, label='Avg Inflation')
ax.bar(x+w, plot_dec['avg_unemployment'], width=w, label='Avg Unemployment')
ax.set_xticks(x); ax.set_xticklabels(plot_dec['Decade'].astype(str))
ax.set_title('Average Macro Conditions by Decade')
ax.set_ylabel('Percent (%)'); ax.legend(); ax.grid(axis='y', alpha=.25)
savefig('05_decade_comparison.png')

# 6. Scatter policy rate vs inflation
pair = df[['Effective Federal Funds Rate','Inflation Rate']].dropna()
plt.figure(figsize=(7,5))
plt.scatter(pair['Inflation Rate'], pair['Effective Federal Funds Rate'], alpha=.45)
plt.title('Federal Funds Rate vs Inflation')
plt.xlabel('Inflation Rate (%)'); plt.ylabel('Effective Fed Funds Rate (%)'); plt.grid(alpha=.25)
savefig('06_policy_vs_inflation_scatter.png')

# 7. Correlation heatmap without seaborn
plt.figure(figsize=(8,6))
plt.imshow(corr, aspect='auto')
plt.colorbar(label='Correlation')
plt.xticks(range(len(corr.columns)), [c.replace(' Rate','').replace('Federal Funds ','Fed ') for c in corr.columns], rotation=45, ha='right')
plt.yticks(range(len(corr.index)), [c.replace(' Rate','').replace('Federal Funds ','Fed ') for c in corr.index])
plt.title('Correlation Matrix')
savefig('07_correlation_matrix.png')

# -------------------- Print senior-analyst observations --------------------
print('\nTop inflation observations:')
print(df.nlargest(10, 'Inflation Rate')[['Date','Inflation Rate','Effective Federal Funds Rate','Unemployment Rate']].to_string(index=False))
print('\nTop policy-rate observations:')
print(df.nlargest(10, 'Effective Federal Funds Rate')[['Date','Effective Federal Funds Rate','Inflation Rate','Unemployment Rate']].to_string(index=False))
print('\nNegative GDP observations:')
print(df[df['Real GDP (Percent Change)'] < 0][['Date','Real GDP (Percent Change)','Inflation Rate','Unemployment Rate']].head(20).to_string(index=False))
print('\nCorrelation matrix:\n', corr.round(3))
