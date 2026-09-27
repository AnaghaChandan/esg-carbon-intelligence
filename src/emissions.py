import pandas as pd


def load_emission_factors(file_path):
    """
    Load emission factors from a CSV file.

    Parameters:
        file_path (str): Path to the emission factors CSV file.

    Returns:
        pandas.DataFrame: Emission factor data.
    """

    factors_df = pd.read_csv(file_path)

    required_columns = {"activity", "emission_factor"}

    missing_columns = required_columns - set(factors_df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns in emission factor file: "
            f"{sorted(missing_columns)}"
        )

    return factors_df


def get_emission_factor(factors_df, activity):
    """
    Retrieve the emission factor for a specific activity.

    Parameters:
        factors_df (pandas.DataFrame): Emission factor data.
        activity (str): Activity name.

    Returns:
        float: Emission factor.

    Raises:
        ValueError: If the activity is missing or has an invalid factor.
    """

    matching_rows = factors_df.loc[
        factors_df["activity"] == activity,
        "emission_factor"
    ]

    if matching_rows.empty:
        raise ValueError(
            f"No emission factor found for activity: '{activity}'"
        )

    factor = matching_rows.iloc[0]

    if pd.isna(factor) or factor < 0:
        raise ValueError(
            f"Invalid emission factor for activity: '{activity}'"
        )

    return float(factor)


def calculate_emissions(activity_df, factors_df):
    """
    Calculate Scope 1, Scope 2, and Scope 3 emissions.

    Formula:

        Emissions = Activity Data × Emission Factor

    Emissions are initially calculated in kgCO2e
    and then converted to tCO2e.

    Parameters:
        activity_df (pandas.DataFrame): Activity data.
        factors_df (pandas.DataFrame): Emission factors.

    Returns:
        pandas.DataFrame: Activity data with calculated emissions.
    """

    df = activity_df.copy()

    # Get emission factors safely
    diesel_factor = get_emission_factor(
        factors_df, "diesel"
    )

    natural_gas_factor = get_emission_factor(
        factors_df, "natural_gas"
    )

    electricity_factor = get_emission_factor(
        factors_df, "electricity"
    )

    business_travel_factor = get_emission_factor(
        factors_df, "business_travel"
    )

    employee_commute_factor = get_emission_factor(
        factors_df, "employee_commute"
    )

    waste_factor = get_emission_factor(
        factors_df, "waste"
    )

    # --------------------------------------------------
    # Calculate emissions in kgCO2e
    # --------------------------------------------------

    df["diesel_emissions_kg"] = (
        df["diesel_liters"] * diesel_factor
    )

    df["natural_gas_emissions_kg"] = (
        df["natural_gas_m3"] * natural_gas_factor
    )

    df["electricity_emissions_kg"] = (
        df["electricity_kwh"] * electricity_factor
    )

    df["business_travel_emissions_kg"] = (
        df["business_travel_km"] * business_travel_factor
    )

    df["employee_commute_emissions_kg"] = (
        df["employee_commute_km"] * employee_commute_factor
    )

    df["waste_emissions_kg"] = (
        df["waste_kg"] * waste_factor
    )

    # --------------------------------------------------
    # Calculate emissions by scope
    # --------------------------------------------------

    # Scope 1: Direct emissions
    df["scope_1_tco2e"] = (
        df["diesel_emissions_kg"]
        + df["natural_gas_emissions_kg"]
    ) / 1000

    # Scope 2: Purchased electricity
    df["scope_2_tco2e"] = (
        df["electricity_emissions_kg"]
    ) / 1000

    # Scope 3: Other indirect emissions
    df["scope_3_tco2e"] = (
        df["business_travel_emissions_kg"]
        + df["employee_commute_emissions_kg"]
        + df["waste_emissions_kg"]
    ) / 1000

    # --------------------------------------------------
    # Total emissions
    # --------------------------------------------------

    df["total_tco2e"] = (
        df["scope_1_tco2e"]
        + df["scope_2_tco2e"]
        + df["scope_3_tco2e"]
    )

    return df