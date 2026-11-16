
import pandas as pd
import matplotlib.pyplot as plt


# 1. Load CSV File
def load_data(filename):

    try:
        df = pd.read_csv(filename)

        required = ["PNR", "Train", "Class", "Fare", "Status"]

        for col in required:
            if col not in df.columns:
                print("Error: Missing column:", col)
                return None

        df["Fare"] = pd.to_numeric(df["Fare"], errors="coerce")

        invalid = df[df["Fare"].isna()]

        for _, row in invalid.iterrows():
            print(
                f"Warning: Row with PNR {row['PNR']} skipped - invalid fare."
            )

        df = df.dropna(subset=["Fare"]).copy()

        print("\nValid records analysed:", len(df))

        return df

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None

    except Exception as e:
        print("Error:", e)
        return None


# 2. Bookings Per Train
def bookings_per_train(df):

    print("\n========== BOOKINGS PER TRAIN ==========")

    bookings = df.groupby("Train").size()

    for train, count in bookings.items():
        print(f"{train} : {count}")

    print("Total bookings:", len(df))

    bookings.plot(kind="bar")
    plt.title("Bookings Per Train")
    plt.xlabel("Train")
    plt.ylabel("Number of Bookings")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show(block=True)


# 3. Revenue Per Train
def revenue_per_train(df):

    print("\n========== REVENUE PER TRAIN ==========")

    confirmed = df[
        df["Status"].astype(str).str.strip().str.lower()
        == "confirmed"
    ]

    revenue = confirmed.groupby("Train")["Fare"].sum()

    for train, amount in revenue.items():
        print(f"{train} : Rs. {amount:g}")

    print(f"Total confirmed revenue: Rs. {revenue.sum():g}")

    revenue.plot(kind="bar")
    plt.title("Confirmed Revenue Per Train")
    plt.xlabel("Train")
    plt.ylabel("Revenue (Rs.)")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show(block=True)


# 4. Ticket Status
def ticket_status(df):

    print("\n========== TICKET STATUS ==========")

    status = df["Status"].astype(str).str.strip().str.lower()

    print("Confirmed :", (status == "confirmed").sum())
    print("Waiting   :", (status == "waiting").sum())
    print("Cancelled :", (status == "cancelled").sum())


# 5. Main Menu
def main():

    filename = input("Enter CSV filename: ").strip()

    df = load_data(filename)

    if df is None:
        return

    while True:

        print("\n====================================")
        print("   RAILWAY RESERVATION ANALYZER")
        print("====================================")

        print("1. Bookings per train")
        print("2. Revenue per train")
        print("3. Ticket status count")
        print("4. Exit")

        choice = input("\nEnter your choice (1-4): ").strip()

        print("Selected option:", repr(choice))

        if choice == "1":
            bookings_per_train(df)

        elif choice == "2":
            revenue_per_train(df)

        elif choice == "3":
            ticket_status(df)

        elif choice == "4":
            print("Exiting program...")
            break

        else:
            print("Invalid choice. Please enter 1, 2, 3 or 4.")


if __name__ == "__main__":
    main()
