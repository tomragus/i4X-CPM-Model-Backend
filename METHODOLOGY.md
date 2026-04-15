# CPM Predictive Analytics — Methodology & Findings

## Dataset
- 211 completed projects with fitted S-curves (2011–2025)
- Total portfolio value: $6.6B
- Source: UCSD CPM eBuilder cashflow exports

## Project Tiers
| Tier | Budget Range | n Projects |
|---|---|---|
| Small | < $250K | 41 |
| Medium | $250K – $5M | 89 |
| Large | $5M – $50M | 60 |
| Mega | > $50M | 21 |

## S-Curve Model
Each project's cumulative spend is fit to a logistic curve:
`L / (1 + exp(-k * (t - t0)))`
- **L**: budget ceiling (= Projected Commitments)
- **k**: growth rate — how steeply spending ramps up
- **t0**: midpoint — when in the project lifetime spending peaks
- Minimum fit quality: R² > 0.75

## Key Findings

### 1. Growth rate decreases with project size
Median k: Small 0.455 → Medium 0.425 → Large 0.358 → Mega 0.179.
Larger projects have more gradual, drawn-out spend curves.
Implication: A PM benchmarking a Mega project against a Medium project
will systematically over-forecast early cash needs.

### 2. Spending peak shifts later as projects grow
Small projects peak at ~40% of project lifetime.
Mega projects peak at ~60%.
Implication: Small projects front-load spending; large projects back-load it.
PMs should adjust cash flow expectations accordingly — not assume a
universal midpoint.

### 3. Large projects are more curve-predictable
Model R²: Small 0.979 → Mega 0.996.
Larger projects follow the logistic pattern more consistently.
Small projects are individually well-fit but highly variable across projects.
Implication: Predictions for small projects carry wider uncertainty bands.

### 4. Mega project envelopes are wide
With n=21, the 10th–90th percentile band spans nearly the full range.
This reflects genuine diversity in Mega project types (housing, research,
healthcare, parking) rather than pure data noise.
Implication: Mega project forecasts should always be presented with wide
confidence intervals and compared to the most similar project type.

## Files
- `eda_tier_analysis.ipynb` — full analysis notebook
- `outputs/training_summary_stats.json` — tier stats for website
- `outputs/growth_rate_vs_size.png`
- `outputs/midpoint_vs_size.png`
- `outputs/tier_distributions.png`
- `outputs/envelope_small/medium/large/mega.png`
  