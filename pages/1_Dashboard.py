import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
import pandas as pd

from src.data_loader import load_activity_data
from src.validation import validate_activity_data
from src.emissions import load_emission_factors, calculate_emissions
from src.insights import (
    company_summary,
    yearly_summary,
    scope_summary,
    carbon_intensity,
    top_emission_sources,
    dashboard_kpis
)

# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="ESG Carbon Intelligence",
    page_icon="🌱",
    layout="wide"
)


# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("🌱 ESG Carbon Intelligence")

st.markdown(
    """
    **Carbon emissions analytics dashboard for monitoring
    Scope 1, Scope 2 and Scope 3 emissions.**
    
    Analyze emissions by company, year, emission scope and
    activity source using calculated carbon metrics.
    """
)

st.caption(
    "Synthetic dataset • Illustrative emission factors • Educational project"
)

st.divider()

# --------------------------------------------------
# Load data
# --------------------------------------------------

st.sidebar.header("📂 Data Source")

uploaded_file = st.sidebar.file_uploader(
    "Upload Activity Data",
    type=["csv", "xlsx"],
    help="Upload a CSV or Excel file containing ESG activity data."
)

if uploaded_file is not None:

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)

    else:
        df = pd.read_excel(uploaded_file)

else:
    df = load_activity_data("data/activity_data.csv")

# Validate activity data
validation_results = validate_activity_data(df)

# Load emission factors
factors_df = load_emission_factors(
    "data/emission_factors.csv"
)

# Calculate emissions
emissions_df = calculate_emissions(
    df,
    factors_df
)

# --------------------------------------------------
# Data Quality Status
# --------------------------------------------------

st.subheader("✅ Data Quality")

has_errors = (
    validation_results["missing_columns"]
    or validation_results["missing_values"]
    or validation_results["invalid_numeric_columns"]
    or validation_results["negative_values"]
    or validation_results["invalid_years"]
)

if has_errors:
    st.warning(
        "Potential data quality issues were detected. "
        "Review the validation details below."
    )

    with st.expander("View Validation Details"):

        if validation_results["missing_columns"]:
            st.write(
                "**Missing Columns:**",
                validation_results["missing_columns"]
            )

        if validation_results["missing_values"]:
            st.write(
                "**Missing Values:**",
                validation_results["missing_values"]
            )

        if validation_results["invalid_numeric_columns"]:
            st.write(
                "**Invalid Numeric Columns:**",
                validation_results["invalid_numeric_columns"]
            )

        if validation_results["negative_values"]:
            st.write(
                "**Negative Activity Values:**",
                validation_results["negative_values"]
            )

        if validation_results["invalid_years"]:
            st.write(
                "**Invalid Years:**",
                validation_results["invalid_years"]
            )

else:
    st.success(
        "All basic data quality checks passed successfully."
    )


# --------------------------------------------------
# Filters
# --------------------------------------------------

st.sidebar.header("🔎 Filters")

companies = sorted(emissions_df["company"].unique())
years = sorted(emissions_df["year"].unique())

selected_companies = st.sidebar.multiselect(
    "Select Company",
    companies,
    default=companies
)

selected_years = st.sidebar.multiselect(
    "Select Year",
    years,
    default=years
)


# Apply filters
filtered_df = emissions_df[
    emissions_df["company"].isin(selected_companies)
    & emissions_df["year"].isin(selected_years)
]


# --------------------------------------------------
# Check filtered data
# --------------------------------------------------

if filtered_df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()


# --------------------------------------------------
# KPIs
# --------------------------------------------------

kpis = dashboard_kpis(filtered_df)

st.subheader("📌 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    label="Total Emissions",
    value=f"{kpis['total_emissions']:,.2f} tCO₂e",
    help="Total estimated greenhouse gas emissions across all selected companies and years."
)

col2.metric(
    label="Scope 1",
    value=f"{kpis['scope_1']:,.2f} tCO₂e",
    help="Direct emissions from sources such as diesel and natural gas."
)

col3.metric(
    label="Scope 2",
    value=f"{kpis['scope_2']:,.2f} tCO₂e",
    help="Emissions associated with purchased electricity."
)

col4.metric(
    label="Scope 3",
    value=f"{kpis['scope_3']:,.2f} tCO₂e",
    help="Selected indirect emissions such as travel, commuting and waste."
)


st.divider()

# --------------------------------------------------
# Data Coverage
# --------------------------------------------------

st.subheader("📊 Data Coverage")

coverage_col1, coverage_col2, coverage_col3 = st.columns(3)

coverage_col1.metric(
    "Companies",
    kpis["companies"]
)

coverage_col2.metric(
    "Years Covered",
    kpis["years"]
)

coverage_col3.metric(
    "Data Records",
    len(filtered_df)
)


# --------------------------------------------------
# Company Analysis
# --------------------------------------------------

st.subheader("🏢 Emissions by Company")

company_data = company_summary(filtered_df)

company_col1, company_col2 = st.columns([1, 1.5])

with company_col1:
    st.dataframe(
        company_data,
        use_container_width=True,
        hide_index=True
    )

with company_col2:
    st.bar_chart(
        company_data.set_index("company")["total_tco2e"]
    )


# --------------------------------------------------
# Yearly Trend
# --------------------------------------------------

st.subheader("📈 Emissions Trend Over Time")

year_data = yearly_summary(filtered_df)

trend_col1, trend_col2 = st.columns([1.5, 1])

with trend_col1:
    st.line_chart(
        year_data.set_index("year")["total_tco2e"]
    )

with trend_col2:
    st.dataframe(
        year_data,
        use_container_width=True,
        hide_index=True
    )

# --------------------------------------------------
# Scope Analysis
# --------------------------------------------------

st.subheader("🌍 Emissions by Scope")

scope_data = scope_summary(filtered_df)

scope_col1, scope_col2 = st.columns([1.5, 1])

with scope_col1:
    st.bar_chart(
        scope_data.set_index("scope")["emissions_tco2e"]
    )

with scope_col2:
    st.dataframe(
        scope_data,
        use_container_width=True,
        hide_index=True
    )


# --------------------------------------------------
# Top Emission Sources
# --------------------------------------------------

st.subheader("🔥 Top Emission Sources")

source_data = top_emission_sources(filtered_df)

source_col1, source_col2 = st.columns([1.5, 1])

with source_col1:
    st.bar_chart(
        source_data.set_index("source")["emissions_tco2e"]
    )

with source_col2:
    st.dataframe(
        source_data,
        use_container_width=True,
        hide_index=True
    )


# --------------------------------------------------
# Carbon Intensity
# --------------------------------------------------

st.subheader("📊 Carbon Intensity")

intensity_data = carbon_intensity(filtered_df)

intensity_col1, intensity_col2 = st.columns(2)

avg_revenue_intensity = intensity_data[
    "tco2e_per_million_usd"
].mean()

avg_employee_intensity = intensity_data[
    "tco2e_per_employee"
].mean()

with intensity_col1:
    st.metric(
        "Average Emissions per $1M Revenue",
        f"{avg_revenue_intensity:,.2f} tCO₂e",
        help="Average emissions intensity relative to company revenue."
    )

with intensity_col2:
    st.metric(
        "Average Emissions per Employee",
        f"{avg_employee_intensity:,.2f} tCO₂e",
        help="Average emissions intensity relative to employee count."
    )

st.dataframe(
    intensity_data,
    use_container_width=True,
    hide_index=True
)

st.caption(
    "Carbon intensity normalizes emissions relative to company revenue "
    "and employee count, helping provide context beyond total emissions."
)


# --------------------------------------------------
# Automated Business Insights
# --------------------------------------------------
st.subheader("💡 Key Business Insights")

highest_company = company_data.iloc[0]
highest_source = source_data.iloc[0]
highest_scope = scope_data.sort_values(
    "emissions_tco2e",
    ascending=False
).iloc[0]

# Calculate year-over-year trend
if len(year_data) >= 2:

    first_year = year_data.iloc[0]
    last_year = year_data.iloc[-1]

    change = (
        (last_year["total_tco2e"] - first_year["total_tco2e"])
        / first_year["total_tco2e"]
    ) * 100

    if change > 0:
        trend_text = (
            f"Total emissions increased by **{change:.2f}%** "
            f"from {int(first_year['year'])} to "
            f"{int(last_year['year'])}."
        )

    elif change < 0:
        trend_text = (
            f"Total emissions decreased by **{abs(change):.2f}%** "
            f"from {int(first_year['year'])} to "
            f"{int(last_year['year'])}."
        )

    else:
        trend_text = (
            "Total emissions remained unchanged across "
            "the selected years."
        )

else:
    trend_text = (
        "Select multiple years to analyze the emissions trend."
    )


insight_col1, insight_col2 = st.columns(2)

with insight_col1:

    st.info(
        f"🏢 **Highest-emitting company**\n\n"
        f"{highest_company['company']} — "
        f"{highest_company['total_tco2e']:,.2f} tCO₂e"
    )

    st.info(
        f"🔥 **Largest emission source**\n\n"
        f"{highest_source['source']} — "
        f"{highest_source['emissions_tco2e']:,.2f} tCO₂e"
    )


with insight_col2:

    st.info(
        f"🌍 **Largest emission scope**\n\n"
        f"{highest_scope['scope']} — "
        f"{highest_scope['emissions_tco2e']:,.2f} tCO₂e"
    )

    st.info(
        f"📈 **Emissions trend**\n\n"
        f"{trend_text}"
    )


# --------------------------------------------------
# Methodology
# --------------------------------------------------

with st.expander("ℹ️ Methodology"):

    st.write(
        """
        Emissions are estimated using the basic calculation:

        **Emissions = Activity Data × Emission Factor**

        The resulting values are converted from kgCO₂e to tCO₂e.

        Scope 1 represents direct emissions, Scope 2 represents
        emissions associated with purchased electricity, and Scope 3
        represents selected indirect value-chain activities.

        The current dataset is synthetic and the emission factors are
        illustrative for educational purposes.
        """
    )
    