import pandas as pd


def company_summary(df):
    """
    Calculate total emissions by company.
    """
    return (
        df.groupby("company")[
            ["scope_1_tco2e", "scope_2_tco2e", "scope_3_tco2e", "total_tco2e"]
        ]
        .sum()
        .reset_index()
        .sort_values("total_tco2e", ascending=False)
    )


def yearly_summary(df):
    """
    Calculate total emissions by year.
    """
    return (
        df.groupby("year")[
            ["scope_1_tco2e", "scope_2_tco2e", "scope_3_tco2e", "total_tco2e"]
        ]
        .sum()
        .reset_index()
        .sort_values("year")
    )


def scope_summary(df):
    """
    Calculate total emissions by scope.
    """
    return pd.DataFrame({
        "scope": ["Scope 1", "Scope 2", "Scope 3"],
        "emissions_tco2e": [
            df["scope_1_tco2e"].sum(),
            df["scope_2_tco2e"].sum(),
            df["scope_3_tco2e"].sum()
        ]
    })


def carbon_intensity(df):
    """
    Calculate carbon intensity based on company revenue
    and number of employees.
    """

    result = df[
        [
            "company",
            "year",
            "total_tco2e",
            "revenue_million_usd",
            "employees"
        ]
    ].copy()

    result["tco2e_per_million_usd"] = (
        result["total_tco2e"] /
        result["revenue_million_usd"]
    )

    result["tco2e_per_employee"] = (
        result["total_tco2e"] /
        result["employees"]
    )

    return result


def top_emission_sources(df):
    """
    Identify the major emission sources.
    """

    sources = {
        "Electricity": df["electricity_emissions_kg"].sum() / 1000,
        "Natural Gas": df["natural_gas_emissions_kg"].sum() / 1000,
        "Diesel": df["diesel_emissions_kg"].sum() / 1000,
        "Employee Commute": df["employee_commute_emissions_kg"].sum() / 1000,
        "Business Travel": df["business_travel_emissions_kg"].sum() / 1000,
        "Waste": df["waste_emissions_kg"].sum() / 1000
    }

    return (
        pd.DataFrame(
            sources.items(),
            columns=["source", "emissions_tco2e"]
        )
        .sort_values("emissions_tco2e", ascending=False)
        .reset_index(drop=True)
    )


def dashboard_kpis(df):
    """
    Generate key performance indicators for the dashboard.
    """

    return {
        "total_emissions": df["total_tco2e"].sum(),
        "scope_1": df["scope_1_tco2e"].sum(),
        "scope_2": df["scope_2_tco2e"].sum(),
        "scope_3": df["scope_3_tco2e"].sum(),
        "companies": df["company"].nunique(),
        "years": df["year"].nunique()
    }