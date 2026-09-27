from src.data_loader import load_activity_data
from src.validation import validate_activity_data


def main():
    file_path = "data/activity_data.csv"

    df = load_activity_data(file_path)
    validation_results = validate_activity_data(df)

    print("ESG Carbon Intelligence")
    print("-----------------------")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")

    print("\nValidation Results:")
    print(validation_results)


if __name__ == "__main__":
    main()