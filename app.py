from src.data_loader import load_activity_data
from src.validation import validate_activity_data
from src.emissions import (
    load_emission_factors,
    calculate_emissions
)
from src.analytics import (
    company_summary,
    yearly_summary,
    scope_summary,
    calculate_carbon_intensity,
    top_emission_sources,
    calculate_kpis
)

def main():

    activity_file = "data/activity_data.csv"
    factors_file = "data/emission_factors.csv"

    # Load data
    activity_df = load_activity_data(activity_file)
    factors_df = load_emission_factors(factors_file)

    # Validate data
    validation_results = validate_activity_data(activity_df)

    print("ESG Carbon Intelligence")
    print("-----------------------")

    print("\nValidation Results:")
    print(validation_results)

    # Calculate emissions
    emissions_df = calculate_emissions(
        activity_df,
        factors_df
    )

    # -----------------------------
    # Analytics
    # -----------------------------

    print("\nCompany Summary:")
    print(company_summary(emissions_df).to_string(index=False))

    print("\nYearly Summary:")
    print(yearly_summary(emissions_df).to_string(index=False))

    print("\nScope Summary:")
    print(scope_summary(emissions_df).to_string(index=False))

    print("\nCarbon Intensity:")
    print(
        calculate_carbon_intensity(emissions_df)[
            [
                "company",
                "year",
                "tco2e_per_million_usd",
                "tco2e_per_employee"
            ]
        ].to_string(index=False)
    )

    print("\nTop Emission Sources:")
    print(
        top_emission_sources(emissions_df)
        .to_string(index=False)
    )

    print("\nDashboard KPIs:")
    print(calculate_kpis(emissions_df))


if __name__ == "__main__":
    main()