
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# ==========================================
# 1. PROJECT SETUP
# ==========================================

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"
CLEAN_DIR = OUTPUT_DIR / "cleaned_data"
CHART_DIR = OUTPUT_DIR / "charts"

CHART_DIR.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid")

# Load cleaned datasets
india = pd.read_csv(CLEAN_DIR / "india_unemployment_cleaned.csv",
                    parse_dates=["date"])

upto_2020 = pd.read_csv(
    CLEAN_DIR / "unemployment_upto_2020_cleaned.csv",
    parse_dates=["date"]
)

RATE = "estimated_unemployment_rate"

# ==========================================
# 2. BASIC ANALYSIS
# ==========================================

print("\n========== BASIC ANALYSIS ==========")

print("Dataset 1 date range:",
      india["date"].min().date(), "to",
      india["date"].max().date())

print("Dataset 2 date range:",
      upto_2020["date"].min().date(), "to",
      upto_2020["date"].max().date())

print("\nOverall average unemployment rate (Dataset 1):",
      round(india[RATE].mean(), 2), "%")

print("Overall average unemployment rate (Dataset 2):",
      round(upto_2020[RATE].mean(), 2), "%")

# ==========================================
# 3. CHART 1: MONTHLY UNEMPLOYMENT TREND
# ==========================================

monthly_trend = (
    india.groupby("date")[RATE]
    .mean()
    .sort_index()
)

plt.figure(figsize=(12, 6))
plt.plot(monthly_trend.index, monthly_trend.values,
         marker="o", linewidth=2)

plt.title("Average Unemployment Rate Over Time - India Dataset")
plt.xlabel("Date")
plt.ylabel("Average unemployment rate (%)")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(CHART_DIR / "01_monthly_unemployment_trend.png",
            dpi=300, bbox_inches="tight")
plt.close()

# ==========================================
# 4. CHART 2: STATE-WISE COMPARISON
# ==========================================

state_rates = (
    upto_2020.groupby("region")[RATE]
    .mean()
    .sort_values(ascending=False)
)

plt.figure(figsize=(12, 8))
sns.barplot(x=state_rates.values, y=state_rates.index)

plt.title("Average Unemployment Rate by Region")
plt.xlabel("Average unemployment rate (%)")
plt.ylabel("Region")
plt.tight_layout()

plt.savefig(CHART_DIR / "02_region_comparison.png",
            dpi=300, bbox_inches="tight")
plt.close()

# ==========================================
# 5. CHART 3: COVID-19 PERIOD TREND
# ==========================================

covid_monthly = (
    upto_2020.groupby(upto_2020["date"].dt.to_period("M"))[RATE]
    .mean()
)

covid_monthly.index = covid_monthly.index.to_timestamp()

plt.figure(figsize=(12, 6))
plt.plot(covid_monthly.index, covid_monthly.values,
         marker="o", color="darkred", linewidth=2)

plt.axvline(pd.Timestamp("2020-03-01"),
            linestyle="--", color="black",
            label="March 2020: pandemic period begins")

plt.title("Monthly Unemployment Rate During 2020")
plt.xlabel("Month")
plt.ylabel("Average unemployment rate (%)")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(CHART_DIR / "03_covid_period_trend.png",
            dpi=300, bbox_inches="tight")
plt.close()

# ==========================================
# 6. CHART 4: RURAL VS URBAN
# ==========================================

if "area" in india.columns:
    area_rates = (
        india.groupby("area")[RATE]
        .mean()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(8, 5))
    sns.barplot(x=area_rates.index, y=area_rates.values)

    plt.title("Average Unemployment Rate: Rural vs Urban")
    plt.xlabel("Area")
    plt.ylabel("Average unemployment rate (%)")
    plt.tight_layout()

    plt.savefig(CHART_DIR / "04_rural_vs_urban.png",
                dpi=300, bbox_inches="tight")
    plt.close()

# ==========================================
# 7. PRINT KEY FINDINGS
# ==========================================

print("\n========== KEY FINDINGS ==========")

print("\nHighest average unemployment regions:")
print(state_rates.head(5).round(2).to_string())

print("\nLowest average unemployment regions:")
print(state_rates.tail(5).sort_values().round(2).to_string())

if len(covid_monthly) > 0:
    peak_month = covid_monthly.idxmax()
    low_month = covid_monthly.idxmin()

    print("\nHighest monthly average in Dataset 2:",
          peak_month.strftime("%B %Y"),
          "-", round(covid_monthly.max(), 2), "%")

    print("Lowest monthly average in Dataset 2:",
          low_month.strftime("%B %Y"),
          "-", round(covid_monthly.min(), 2), "%")

print("\nRural vs Urban average rates:")
if "area" in india.columns:
    print(area_rates.round(2).to_string())

print("\nCharts saved successfully in:", CHART_DIR)
print("========== ANALYSIS COMPLETED ==========")

# ========== COVID-PERIOD COMPARISON ==========

# Ensure the reports folder exists
REPORT_DIR = BASE_DIR / "outputs" / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# Group observations into three time periods
def classify_period(date):
    if date.month in [1, 2] and date.year == 2020:
        return "Pre-pandemic reference (Jan-Feb 2020)"
    elif date.month in [3, 4, 5, 6] and date.year == 2020:
        return "Early pandemic (Mar-Jun 2020)"
    elif date.month in [7, 8, 9, 10] and date.year == 2020:
        return "Later 2020 (Jul-Oct 2020)"
    else:
        return "Outside comparison period"

upto_2020["period"] = upto_2020["date"].apply(classify_period)

# Calculate descriptive statistics for each period
period_summary = (
    upto_2020[upto_2020["period"] != "Outside comparison period"]
    .groupby("period", observed=False)[RATE]
    .agg(["mean", "median", "min", "max", "count"])
    .reset_index()
)

# Round numerical results
period_summary[["mean", "median", "min", "max"]] = (
    period_summary[["mean", "median", "min", "max"]].round(2)
)

# Save the summary as a CSV report
summary_path = REPORT_DIR / "covid_period_comparison.csv"
period_summary.to_csv(summary_path, index=False)

# Create a comparison chart
plt.figure(figsize=(10, 6))
sns.barplot(data=period_summary, x="period", y="mean")
plt.title("Average Unemployment Rate by COVID-19 Period")
plt.xlabel("Period")
plt.ylabel("Average unemployment rate (%)")
plt.xticks(rotation=15, ha="right")
plt.tight_layout()

chart_path = CHART_DIR / "05_covid_period_comparison.png"
plt.savefig(chart_path, dpi=300, bbox_inches="tight")
plt.close()

print("\n========== COVID-PERIOD COMPARISON ==========")
print(period_summary.to_string(index=False))
print(f"\nSummary CSV saved to: {summary_path}")
print(f"Comparison chart saved to: {chart_path}")
