
def parse_rental(text):
    if not isinstance(text, str) or text.count(":") != 1:
        raise ValueError("Input must be in unit:months format")

    unit, months = text.split(":")
    if not unit.strip() or not months.strip():
        raise ValueError("Unit and months cannot be empty")

    try:
        months = float(months)
    except ValueError:
        raise ValueError("Months must be numeric")

    return unit.strip().title(), months


def duration_average(months_csv):
    if not isinstance(months_csv, str) or not months_csv.strip():
        raise ValueError("Enter a non-empty comma-separated list")

    try:
        values = [int(value.strip()) for value in months_csv.split(",")]
    except ValueError:
        raise ValueError("All durations must be integers")

    if not values:
        raise ValueError("At least one duration is required")

    return sum(values) // len(values)


def payable_rent(text):
    if not isinstance(text, str) or text.count("|") != 1:
        raise ValueError("Input must be in rent|discount format")

    rent, discount = text.split("|")

    try:
        rent = float(rent)
        discount = float(discount)
    except ValueError:
        raise ValueError("Rent and discount must be numeric")

    return max(rent * 1.18 - discount, 0)


def main():
    print("==== Running parse_rental ====")
    user_input = input("Enter unit:months (e.g. medium:6): ")
    print("Unit and Months:", parse_rental(user_input))

    print("\n==== Running duration_average ====")
    user_input = input("Enter rental months as CSV (e.g. 3,6,12): ")
    print("Average Duration:", duration_average(user_input))

    print("\n==== Running payable_rent ====")
    user_input = input("Enter rent|discount (e.g. 2400|200): ")
    print("Payable Rent:", payable_rent(user_input))


if __name__ == "__main__":
    main()
