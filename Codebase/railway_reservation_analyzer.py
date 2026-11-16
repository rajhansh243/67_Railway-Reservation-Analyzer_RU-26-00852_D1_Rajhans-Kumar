 
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# --------------------------------
# 1. Read CSV File
# --------------------------------

def load_data(filename):

    file_path = Path(filename)

    # Also check the Testcases folder
    if not file_path.exists():
        file_path = Path("Testcases") / filename

    # Check the folder containing this Python file
    if not file_path.exists():
        file_path = Path(__file__).resolve().parent / filename

    if not file_path.exists():
        file_path = (
            Path(__file__).resolve().parent.parent
            / "Testcases" / filename
        )

    try:
        df = pd.read_csv(file_path, dtype=str)

        required_columns = [
            "PNR", "Train", "Class", "Fare", "Status"
        ]

        for column in required_columns:
            if column not in df.columns:
                print(f"Error: Missing column '{column}'.")
                return None

        # Remove extra spaces
        df["PNR"] = df["PNR"].str.strip()
        df["Train"] = df["Train"].str.strip()
        df["Status"] = df["Status"].str.strip().str.title()

        # Convert Fare into numeric values
        df["Fare"] = pd.to_numeric(
            df["Fare"], errors="coerce"
        )

        # Identify invalid fares
        invalid_rows = df[
            df["Fare"].isna() | (df["Fare"] < 0)
        ]

        for _, row in invalid_rows.iterrows():
            print(
                f"Warning: Row with PNR {row['PNR']} "
                f"skipped - invalid fare."
            )

        # Remove invalid fare rows
        df = df.drop(invalid_rows.index).copy()

        print(
            f"\nValid records analysed: {len(df)}"
        )

        return df

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None

    except pd.errors.EmptyDataError:
        print("Error: CSV file is empty.")
        return None

    except Exception as e:
        print("Error:", e)
        return None


# --------------------------------
# 2. Bookings Per Train
# --------------------------------

def bookings_per_train(df):

    print("\n--- Bookings Per Train ---")

    bookings = df.groupby("Train").size()

    for train, count in bookings.items():
        print(f"{train} : {count}")

    print(f"\nTotal bookings: {len(df)}")

    # Bar Chart
    bookings.plot(kind="bar")

    plt.title("Bookings Per Train")
    plt.xlabel("Train")
    plt.ylabel("Number of Bookings")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()


# --------------------------------
# 3. Revenue Per Train
# --------------------------------

def revenue_per_train(df):

    print("\n--- Revenue Per Train ---")

    # Only Confirmed tickets
    confirmed = df[
        df["Status"].str.casefold() == "confirmed"
    ]

    revenue = confirmed.groupby("Train")["Fare"].sum()

    for train, amount in revenue.items():
        print(f"{train} : Rs. {amount:g}")

    total_revenue = confirmed["Fare"].sum()

    print(
        f"\nTotal confirmed revenue: Rs. {total_revenue:g}"
    )

    # Bar Chart
    revenue.plot(kind="bar")

    plt.title("Revenue Per Train")
    plt.xlabel("Train")
    plt.ylabel("Revenue (Rs.)")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()


# --------------------------------
# 4. Ticket Status Count
# --------------------------------

def ticket_status_count(df):

    print("\n--- Ticket Status Count ---")

    status_count = (
        df.groupby("Status")
        .size()
        .reindex(
            ["Confirmed", "Waiting", "Cancelled"],
            fill_value=0
        )
    )

    for status, count in status_count.items():
        print(f"{status} : {count}")

    status_count.plot(kind="bar")

    plt.title("Ticket Status Count")
    plt.xlabel("Status")
    plt.ylabel("Number of Tickets")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()


# --------------------------------
# 5. Main Menu
# --------------------------------

def main():

    print("===================================")
    print("   RAILWAY RESERVATION ANALYZER")
    print("===================================")

    filename = input(
        "\nEnter CSV file name "
        "(default: bookings.csv): "
    ).strip()

    if not filename:
        filename = "bookings.csv"

    df = load_data(filename)

    if df is None:
        return

    while True:

        print("\n========== MAIN MENU ==========")
        print("1. Bookings per train")
        print("2. Revenue per train")
        print("3. Ticket status count")
        print("4. Exit")

        choice = input("\nEnter your choice (1-4): ")

        if choice == "1":
            bookings_per_train(df)

        elif choice == "2":
            revenue_per_train(df)

        elif choice == "3":
            ticket_status_count(df)

        elif choice == "4":
            print("\nThank you for using Railway Reservation Analyzer!")
            break

        else:
            print("Invalid choice! Please enter 1-4.")


# --------------------------------
# Program Execution
# --------------------------------

if __name__ == "__main__":
    main()

