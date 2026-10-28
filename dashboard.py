
from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px

# ---------- PAGE CONFIGURATION ----------
st.set_page_config(
    page_title="Unemployment Analysis in India",
    page_icon="📊",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "outputs" / "cleaned_data"

FILE_1 = DATA_DIR / "india_unemployment_cleaned.csv"
FILE_2 = DATA_DIR / "unemployment_upto_2020_cleaned.csv"

RATE = "estimated_unemployment_rate"
REGION = "region"
DATE = "date"

st.title("🇮🇳 Unemployment Analysis in India")
st.caption(
    "Interactive exploration of unemployment observations, "
    "regional differences, and trends during 2020."
)

# ---------- LOAD DATA ----------
@st.cache_data
def load_data(path):
    df = pd.read_csv(path, parse_dates=[DATE])
    df[REGION] = df[REGION].astype(str).str.strip().str.title()
    df[RATE] = pd.to_numeric(df[RATE], errors="coerce")
    df = df.dropna(subset=[DATE, REGION, RATE])
    return df

if not FILE_1.exists() or not FILE_2.exists():
    st.error(
        "Cleaned CSV files not found. Run main.py first "
        "and check outputs/cleaned_data/."
    )
    st.stop()

df1 = load_data(FILE_1)
df2 = load_data(FILE_2)

# ---------- SIDEBAR FILTERS ----------
st.sidebar.header("Dashboard Filters")

regions = sorted(df2[REGION].dropna().unique())
selected_regions = st.sidebar.multiselect(
    "Select regions",
    options=regions,
    default=regions
)

start_date = df2[DATE].min().date()
end_date = df2[DATE].max().date()

date_range = st.sidebar.date_input(
    "Select date range",
    value=(start_date, end_date),
    min_value=start_date,
    max_value=end_date
)

if len(date_range) != 2:
    st.info("Select both a start date and an end date.")
    st.stop()

start, end = date_range

filtered = df2[
    df2[REGION].isin(selected_regions)
    & df2[DATE].dt.date.between(start, end)
].copy()

if filtered.empty:
    st.warning("No data matches these filters. Change your selections.")
    st.stop()

# ---------- KPI CARDS ----------
average_rate = filtered[RATE].mean()
region_averages = filtered.groupby(REGION)[RATE].mean()

highest_region = region_averages.idxmax()
lowest_region = region_averages.idxmin()

c1, c2, c3 = st.columns(3)

c1.metric("Average unemployment rate", f"{average_rate:.2f}%")
c2.metric(
    "Highest regional average",
    f"{region_averages.max():.2f}%",
    highest_region
)
c3.metric(
    "Lowest regional average",
    f"{region_averages.min():.2f}%",
    lowest_region
)

st.caption(
    "KPIs represent unweighted averages of the selected regional "
    "records, not official population-weighted national estimates."
)

# ---------- MONTHLY TREND ----------
st.subheader("1. Monthly Unemployment Trend")

monthly = (
    filtered.assign(month=filtered[DATE].dt.to_period("M").dt.to_timestamp())
    .groupby("month", as_index=False)[RATE]
    .mean()
)

fig_trend = px.line(
    monthly,
    x="month",
    y=RATE,
    markers=True,
    title="Average recorded unemployment rate over time"
)
fig_trend.update_layout(
    xaxis_title="Month",
    yaxis_title="Average unemployment rate (%)"
)
st.plotly_chart(fig_trend, use_container_width=True)

# ---------- REGIONAL COMPARISON ----------
st.subheader("2. Regional Comparison")

regional = (
    filtered.groupby(REGION, as_index=False)[RATE]
    .mean()
    .sort_values(RATE, ascending=False)
)

fig_regions = px.bar(
    regional,
    x=REGION,
    y=RATE,
    title="Average unemployment rate by region"
)
fig_regions.update_layout(
    xaxis_title="Region",
    yaxis_title="Average unemployment rate (%)",
    xaxis_tickangle=-45
)
st.plotly_chart(fig_regions, use_container_width=True)

# ---------- RURAL VS URBAN ----------
st.subheader("3. Rural vs Urban Comparison")

if "area" in df1.columns:
    area_data = df1.copy()

    if selected_regions:
        area_data = area_data[
            area_data[REGION].isin(selected_regions)
        ]
    else:
        area_data = area_data.iloc[0:0]

    area_summary = (
        area_data.groupby("area", as_index=False)[RATE]
        .mean()
    )

    if not area_summary.empty:
        fig_area = px.bar(
            area_summary,
            x="area",
            y=RATE,
            title="Average unemployment rate by area"
        )
        st.plotly_chart(fig_area, use_container_width=True)
    else:
        st.info("No rural/urban records match the selected regions.")
else:
    st.info("The first dataset does not contain an area column.")

# ---------- COVID PERIOD COMPARISON ----------
st.subheader("4. COVID-Period Comparison")

covid = df2.copy()

covid["period"] = pd.NA
covid.loc[
    (covid[DATE].dt.year == 2020)
    & (covid[DATE].dt.month.isin([1, 2])),
    "period"
] = "Jan-Feb 2020"

covid.loc[
    (covid[DATE].dt.year == 2020)
    & (covid[DATE].dt.month.isin([3, 4, 5, 6])),
    "period"
] = "Mar-Jun 2020"

covid.loc[
    (covid[DATE].dt.year == 2020)
    & (covid[DATE].dt.month.isin([7, 8, 9, 10])),
    "period"
] = "Jul-Oct 2020"

period_order = ["Jan-Feb 2020", "Mar-Jun 2020", "Jul-Oct 2020"]

covid = covid[
    covid["period"].notna()
    & covid[REGION].isin(selected_regions)
]

period_summary = (
    covid.groupby("period")[RATE]
    .mean()
    .reindex(period_order)
    .dropna()
    .rename("Average unemployment rate (%)")
    .reset_index()
)

fig_period = px.bar(
    period_summary,
    x="period",
    y="Average unemployment rate (%)",
    title="Average recorded unemployment rate by period"
)
st.plotly_chart(fig_period, use_container_width=True)

# ---------- DATA TABLE AND DOWNLOAD ----------
st.subheader("5. Filtered Data")

st.dataframe(filtered, use_container_width=True)

csv_data = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download filtered data as CSV",
    data=csv_data,
    file_name="filtered_unemployment_data.csv",
    mime="text/csv"
)

st.caption(
    "Data source: supplied unemployment datasets. "
    "This dashboard describes recorded observations and does not "
    "establish that any event caused a change in unemployment."
)
