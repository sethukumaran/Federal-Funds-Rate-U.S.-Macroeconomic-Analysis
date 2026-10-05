# Federal Funds Rate & U.S. Macroeconomic Analysis

## 1. Executive Summary

This project analyzes a historical U.S. macroeconomic dataset covering **July 1954 to March 2017**. The dataset combines Federal Reserve policy-rate measures with real GDP growth, unemployment and inflation indicators.

The objective is to move beyond descriptive statistics and answer business-style questions such as:

- How did monetary policy evolve across economic cycles?
- When were the highest inflation and interest-rate regimes observed?
- How are policy rates associated with inflation and labor-market conditions?
- Which periods represent macroeconomic stress?
- What data-quality limitations must be considered before using the dataset for forecasting or executive reporting?

> **Important analytical caveat:** the dataset is a historical macroeconomic time series, not a company/business operating dataset. Therefore, “business insights” should be interpreted as insights useful for **corporate planning, treasury, pricing, investment, risk management and scenario planning**.


## 2. Dataset Overview

| Metric | Value |
|---|---:|
| Rows | 904 |
| Columns | 10 original fields |
| Coverage | 1954-07-01 to 2017-03-16 |
| Duplicate rows | 0 |
| Effective Fed Funds Rate observations | 752 |
| Inflation observations | 710 |
| Unemployment observations | 752 |
| Real GDP growth observations | 250 |
| Maximum effective Fed Funds Rate | 19.10% |
| Maximum inflation rate | 13.60% |
| Maximum unemployment rate | 10.80% |
| Minimum real GDP growth | -10.00% |

The original file contains a mixture of monthly and event-date observations. Real GDP growth is quarterly in nature, while several other indicators are monthly. This explains a substantial portion of the missing-value pattern and means the data should **not** be treated as a perfectly balanced monthly panel without transformation.


## 3. Data Dictionary

| Column | Business Meaning |
|---|---|
| Year | Calendar year |
| Month | Calendar month |
| Day | Observation day |
| Federal Funds Target Rate | Historical federal funds target rate where available |
| Federal Funds Upper Target | Upper bound of target range in later regime |
| Federal Funds Lower Target | Lower bound of target range in later regime |
| Effective Federal Funds Rate | Market-effective federal funds rate |
| Real GDP (Percent Change) | Real GDP growth rate observation |
| Unemployment Rate | U.S. unemployment rate |
| Inflation Rate | Inflation rate |


## 4. Data Quality Assessment

### Strengths

- No duplicate rows were detected.
- Dates can be reconstructed reliably from Year, Month and Day.
- Numeric fields are already stored as numeric types.
- The dataset spans multiple monetary-policy regimes, making it useful for historical scenario analysis.

### Key limitations

1. **Missing values are material.** Target-rate fields are unavailable for much of the earlier history, while GDP is only available quarterly.
2. **Frequency mismatch.** GDP observations occur quarterly while unemployment, inflation and effective rates are more frequent.
3. **Policy-regime change.** Target-rate reporting changes over history; the upper/lower target fields become especially relevant in the later period.
4. **Causality cannot be inferred from correlation.** A higher federal funds rate can coincide with high inflation because policy responds to inflation; correlation alone does not prove that higher rates caused inflation.
5. **No external recession label is included.** Negative GDP growth is useful as a stress indicator but should not automatically be treated as an official recession definition.


## 5. Senior Analyst Business Insights

### Insight 1 — Inflation shocks were accompanied by aggressive monetary tightening

The historical maximum inflation observation is **13.6% in June 1980**, while the effective federal funds rate reached **19.10% in June 1981**. The dataset therefore captures a period in which monetary policy became extremely restrictive as policymakers responded to severe inflationary pressure.

**Business implication:** Companies operating in high-inflation environments should not evaluate financing costs, pricing, capital expenditure or inventory decisions using only current interest rates. Historical stress regimes show that financing costs can rise dramatically during inflationary episodes.

### Insight 2 — Interest-rate exposure is a major planning variable

The effective federal funds rate ranges from approximately **0.07% to 19.10%**. That is a very large historical range.

**Business implication:** Businesses with floating-rate debt, refinancing needs or interest-sensitive capital projects should run scenario models across multiple rate environments rather than relying on a single base-case rate.

### Insight 3 — The policy rate and inflation move together strongly in the historical sample

The pairwise correlation between the effective federal funds rate and inflation is approximately **0.784** in the supplied data.

This is a strong positive association, but it must be interpreted carefully: central-bank policy responds to economic conditions, so the relationship reflects both policy reaction and macroeconomic dynamics.

**Business implication:** Inflation should be treated as an important input to treasury and pricing scenarios, but rate forecasts should not be mechanically derived from contemporaneous inflation alone.

### Insight 4 — Labor-market conditions matter for policy and business planning

The maximum unemployment rate in the dataset is **10.8%**. Unemployment and inflation are positively correlated in this dataset, although the relationship is much weaker than the policy-rate/inflation relationship.

**Business implication:** Demand planning should consider both the cost-of-capital environment and labor-market conditions. High unemployment can indicate weaker consumer demand even when inflation remains elevated.

### Insight 5 — GDP volatility creates a direct operating-risk signal

Real GDP growth ranges from **-10.0% to 16.5%** in the observations available.

**Business implication:** GDP growth can be used as a macro scenario variable for revenue planning. A negative-growth scenario should trigger sensitivity analysis for sales volume, collections, inventory and hiring.

### Insight 6 — Historical macro regimes are more useful than a single long-run average

Averages across the entire 1954–2017 period hide major regime changes. The dataset includes low-rate environments, high-inflation/high-rate periods and later low-rate conditions.

**Business implication:** Strategic planning should use regime-based scenarios such as:
- Low inflation / low rates
- Moderate inflation / normal rates
- High inflation / aggressive tightening
- High unemployment / weak growth
rather than using one historical average as the expected future state.


## 6. Recommended Business Use Cases

### Treasury & Finance
- Floating-rate debt sensitivity analysis
- Refinancing risk assessment
- Interest-expense scenario planning
- Cash-management strategy

### Corporate Strategy
- GDP-linked demand scenarios
- Market-entry timing
- Capital expenditure hurdle-rate analysis
- Long-term strategic planning

### Pricing & Commercial Analytics
- Inflation-adjusted pricing scenarios
- Supplier-cost planning
- Margin protection analysis
- Contract escalation assumptions

### Risk Management
- Macro stress testing
- Liquidity planning
- Downside scenario design
- Early-warning dashboards


## 7. SQL Analysis

`analysis.sql` contains SQLite-compatible queries covering:

1. Dataset coverage
2. Missing-value profiling
3. Annual macro dashboard
4. Highest inflation periods
5. Highest interest-rate periods
6. High-inflation regime analysis
7. Low-unemployment regime analysis
8. Negative GDP observations
9. Decade-level comparison
10. Policy tightening/easing detection
11. Macro stress screening
12. Inflation vs policy-rate relationship

### Suggested SQL workflow

1. Import `cleaned_fed_macro_data.csv` into a SQL database as `fed_macro`.
2. Execute the queries in `analysis.sql`.
3. Export the annual and regime-level outputs for Power BI/Tableau/Excel.
4. Build an executive dashboard around rates, inflation, unemployment and GDP.



## 8. Python Analysis

`analysis.py` performs:

- Data loading
- Schema/type inspection
- Missing-value analysis
- Duplicate checks
- Date construction
- Feature engineering
- Annual aggregation
- Decade aggregation
- Correlation analysis
- Macro-stress screening
- Time-series visualization
- Scatter analysis
- Correlation visualization
- Export of cleaned and aggregated datasets

### Visualizations generated

- Effective federal funds rate over time
- Inflation vs policy rate
- Unemployment trend
- Real GDP growth
- Decade-level macro comparison
- Policy rate vs inflation scatter plot
- Correlation matrix# Federal-Funds-Rate-U.S.-Macroeconomic-Analysis
This project analyzes a historical U.S. macroeconomic dataset covering **July 1954 to March 2017**. The dataset combines Federal Reserve policy-rate measures with real GDP growth, unemployment and inflation indicators.

## 9. Conclusion

The analysis demonstrates that U.S. monetary policy, inflation, labor-market conditions and economic growth are tightly connected components of the macroeconomic environment. The strongest business lesson is that **historical averages are not sufficient for planning**. The dataset contains radically different regimes, from very high inflation and interest rates to very low-rate environments.

For a business, the practical response is to translate macroeconomic uncertainty into **scenario-based financial planning**. Treasury teams should stress-test financing costs; commercial teams should test pricing and demand assumptions; strategy teams should incorporate GDP and unemployment scenarios; and risk teams should monitor inflation and policy-rate changes as early-warning indicators.

The next analytical step would be to combine this dataset with company-level revenue, debt, pricing and industry data. That would allow the macro indicators to be converted from general economic signals into measurable business impact and forecasting models.
