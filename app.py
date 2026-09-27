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


def main():

    print("ESG Carbon Intelligence")
    print("=" * 30)

    # 1. Load activity data
    df = load_activity_data("data/activity_data.csv")

    # 2. Validate data
    validation_results = validate_activity_data(df)

    print("\nValidation Results:")
    print(validation_results)

    # 3. Load emission factors
    factors_df = load_emission_factors("data/emission_factors.csv")

    # 4. Calculate emissions
    emissions_df = calculate_emissions(df, factors_df)

    print("\nEmission Results:")
    print(
        emissions_df[
            [
                "company",
                "year",
                "scope_1_tco2e",
                "scope_2_tco2e",
                "scope_3_tco2e",
                "total_tco2e"
            ]
        ]
    )

    # 5. Company summary
    print("\nCompany Summary:")
    print(company_summary(emissions_df))

    # 6. Yearly summary
    print("\nYearly Summary:")
    print(yearly_summary(emissions_df))

    # 7. Scope summary
    print("\nScope Summary:")
    print(scope_summary(emissions_df))

    # 8. Carbon intensity
    print("\nCarbon Intensity:")
    print(carbon_intensity(emissions_df))

    # 9. Top emission sources
    print("\nTop Emission Sources:")
    print(top_emission_sources(emissions_df))

    # 10. Dashboard KPIs
    print("\nDashboard KPIs:")
    print(dashboard_kpis(emissions_df))


if __name__ == "__main__":
    main()