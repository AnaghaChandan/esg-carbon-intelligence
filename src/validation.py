import pandas as pd


REQUIRED_COLUMNS = [
    "company",
    "year",
    "electricity_kwh",
    "diesel_liters",
    "natural_gas_m3",
    "business_travel_km",
    "employee_commute_km",
    "waste_kg",
    "revenue_million_usd",
    "employees",
]


NUMERIC_COLUMNS = [
    "year",
    "electricity_kwh",
    "diesel_liters",
    "natural_gas_m3",
    "business_travel_km",
    "employee_commute_km",
    "waste_kg",
    "revenue_million_usd",
    "employees",
]


ACTIVITY_COLUMNS = [
    "electricity_kwh",
    "diesel_liters",
    "natural_gas_m3",
    "business_travel_km",
    "employee_commute_km",
    "waste_kg",
]
def validate_activity_data(df):
    """
    Validate ESG activity data.

    Returns a dictionary containing validation results.
    """

    results = {
        "missing_columns": [],
        "missing_values": {},
        "duplicate_rows": 0,
        "invalid_numeric_columns": [],
        "negative_values": {},
        "invalid_years": [],
    }

    # Check required columns
    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    results["missing_columns"] = missing_columns

    # Check missing values
    available_required_columns = [
        column for column in REQUIRED_COLUMNS
        if column in df.columns
    ]
    missing_values = df[available_required_columns].isnull().sum()

    results["missing_values"] = {
        column: int(count)
        for column, count in missing_values.items()
        if count > 0
    }

    # Check duplicate rows
    results["duplicate_rows"] = int(df.duplicated().sum())

    # Check numeric columns
    for column in NUMERIC_COLUMNS:
        if column in df.columns:
            if not pd.api.types.is_numeric_dtype(df[column]):
                results["invalid_numeric_columns"].append(column)

    # Check negative activity values
    for column in ACTIVITY_COLUMNS:
        if column in df.columns:
            negative_count = int((df[column] < 0).sum())

            if negative_count > 0:
                results["negative_values"][column] = negative_count

    # Check years
    if "year" in df.columns:
        invalid_years = df.loc[
            ~df["year"].between(2000, 2100),
            "year"
        ].dropna().unique().tolist()

        results["invalid_years"] = invalid_years

    return results