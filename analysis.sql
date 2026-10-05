-- Federal Funds & U.S. Macroeconomic Indicators

-- 1. Dataset coverage and row count
SELECT COUNT(*) AS row_count,
       MIN(Date) AS start_date,
       MAX(Date) AS end_date
FROM fed_macro;

-- 2. Missing-data profile
SELECT
  SUM(CASE WHEN [Effective Federal Funds Rate] IS NULL THEN 1 ELSE 0 END) AS missing_effective_rate,
  SUM(CASE WHEN [Inflation Rate] IS NULL THEN 1 ELSE 0 END) AS missing_inflation,
  SUM(CASE WHEN [Unemployment Rate] IS NULL THEN 1 ELSE 0 END) AS missing_unemployment,
  SUM(CASE WHEN [Real GDP (Percent Change)] IS NULL THEN 1 ELSE 0 END) AS missing_gdp
FROM fed_macro;

-- 3. Annual macro dashboard
SELECT Year,
       ROUND(AVG([Effective Federal Funds Rate]),2) AS avg_fed_funds_rate,
       ROUND(AVG([Inflation Rate]),2) AS avg_inflation,
       ROUND(AVG([Unemployment Rate]),2) AS avg_unemployment,
       ROUND(AVG([Real GDP (Percent Change)]),2) AS avg_real_gdp_growth
FROM fed_macro
GROUP BY Year
ORDER BY Year;

-- 4. Highest inflation periods
SELECT Date, [Inflation Rate], [Effective Federal Funds Rate], [Unemployment Rate]
FROM fed_macro
WHERE [Inflation Rate] IS NOT NULL
ORDER BY [Inflation Rate] DESC
LIMIT 10;

-- 5. Highest federal funds rate periods
SELECT Date, [Effective Federal Funds Rate], [Inflation Rate], [Unemployment Rate]
FROM fed_macro
WHERE [Effective Federal Funds Rate] IS NOT NULL
ORDER BY [Effective Federal Funds Rate] DESC
LIMIT 10;

-- 6. High-inflation regime: >= 6%
SELECT COUNT(*) AS observations,
       ROUND(AVG([Effective Federal Funds Rate]),2) AS avg_policy_rate,
       ROUND(AVG([Unemployment Rate]),2) AS avg_unemployment,
       ROUND(AVG([Inflation Rate]),2) AS avg_inflation
FROM fed_macro
WHERE [Inflation Rate] >= 6;

-- 7. Low-unemployment regime: < 5%
SELECT COUNT(*) AS observations,
       ROUND(AVG([Effective Federal Funds Rate]),2) AS avg_policy_rate,
       ROUND(AVG([Inflation Rate]),2) AS avg_inflation,
       ROUND(AVG([Unemployment Rate]),2) AS avg_unemployment
FROM fed_macro
WHERE [Unemployment Rate] < 5;

-- 8. Negative GDP-growth observations
SELECT Date, [Real GDP (Percent Change)], [Inflation Rate],
       [Unemployment Rate], [Effective Federal Funds Rate]
FROM fed_macro
WHERE [Real GDP (Percent Change)] < 0
ORDER BY Date;

-- 9. Decade-level comparison
SELECT Decade,
       ROUND(AVG([Effective Federal Funds Rate]),2) AS avg_policy_rate,
       ROUND(AVG([Inflation Rate]),2) AS avg_inflation,
       ROUND(AVG([Unemployment Rate]),2) AS avg_unemployment,
       ROUND(MAX([Effective Federal Funds Rate]),2) AS peak_policy_rate,
       ROUND(MAX([Inflation Rate]),2) AS peak_inflation
FROM fed_macro
GROUP BY Decade
ORDER BY Decade;

-- 10. Policy tightening/loosening observations using monthly change
SELECT Date,
       [Effective Federal Funds Rate],
       [Effective_Rate_Change],
       CASE
         WHEN [Effective_Rate_Change] >= 0.50 THEN 'Strong tightening'
         WHEN [Effective_Rate_Change] <= -0.50 THEN 'Strong easing'
         ELSE 'Normal movement'
       END AS policy_move
FROM fed_macro
WHERE [Effective_Rate_Change] IS NOT NULL
ORDER BY ABS([Effective_Rate_Change]) DESC;

-- 11. Macro stress screen: inflation, unemployment or negative growth
SELECT Date,
       [Inflation Rate],
       [Unemployment Rate],
       [Real GDP (Percent Change)],
       [Effective Federal Funds Rate]
FROM fed_macro
WHERE [Inflation Rate] >= 6
   OR [Unemployment Rate] >= 8
   OR [Real GDP (Percent Change)] < 0
ORDER BY Date;

-- 12. Inflation vs policy-rate relationship (pairwise observations)
SELECT COUNT(*) AS paired_observations,
       ROUND(AVG([Inflation Rate]),2) AS avg_inflation,
       ROUND(AVG([Effective Federal Funds Rate]),2) AS avg_policy_rate
FROM fed_macro
WHERE [Inflation Rate] IS NOT NULL
  AND [Effective Federal Funds Rate] IS NOT NULL;
