
import csv
from datetime import datetime


# Hardcoded stock prices for the portfolio tracker.
stock_prices = {"AAPL": 180, "TSLA": 250, "GOOGL": 140, "MSFT": 320, "AMZN": 175}


def get_user_input():
    """Collect stock symbols and quantities from the user until they type 'done'."""
    holdings = []

    while True:
        symbol = input("Enter a stock symbol (or 'done' to finish): ").strip().upper()

        if symbol == "DONE":
            break

        if symbol not in stock_prices and symbol != "DONE":
            print(f"Invalid stock symbol. Try one of: {', '.join(stock_prices.keys())}")
            continue

        quantity_input = input(f"Enter quantity for {symbol}: ").strip()

        try:
            quantity = int(quantity_input)
        except ValueError:
            print("Quantity must be a positive integer.")
            continue

        if quantity <= 0:
            print("Quantity must be a positive integer.")
            continue

        holdings.append({"symbol": symbol, "quantity": quantity})

    return holdings


def calculate_totals(holdings):
    """Calculate the value for each holding and the total portfolio value."""
    rows = []
    total_value = 0

    for holding in holdings:
        price = stock_prices[holding["symbol"]]
        value = price * holding["quantity"]
        total_value += value

        rows.append({
            "symbol": holding["symbol"],
            "quantity": holding["quantity"],
            "price": price,
            "total_value": value,
        })

    return rows, total_value


def display_summary(rows, total_value):
    """Print a clean summary table for the portfolio."""
    print("\nPortfolio Summary")
    print("-" * 60)
    print(f"{'Stock':<10}{'Quantity':<10}{'Price':<10}{'Total Value':<15}")
    print("-" * 60)

    for row in rows:
        print(f"{row['symbol']:<10}{row['quantity']:<10}{row['price']:<10}{row['total_value']:<15}")

    print("-" * 60)
    print(f"{'Total':<10}{'':<10}{'':<10}{total_value:<15}")


def save_to_file(rows, total_value):
    """Save the portfolio summary to a text or CSV file with a timestamp."""
    while True:
        choice = input("Would you like to save the results to a file? (y/n): ").strip().lower()

        if choice in {"n", "no"}:
            print("Results were not saved.")
            return

        if choice not in {"y", "yes"}:
            print("Please enter 'y' or 'n'.")
            continue

        format_choice = input("Choose a file format (txt or csv): ").strip().lower()

        if format_choice not in {"txt", "csv"}:
            print("Invalid format. Please choose txt or csv.")
            continue

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"portfolio_summary_{timestamp}.{format_choice}"

        if format_choice == "txt":
            with open(filename, "w", encoding="utf-8") as file:
                file.write("Stock Portfolio Tracker\n")
                file.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                file.write("Stock | Quantity | Price | Total Value\n")
                for row in rows:
                    file.write(
                        f"{row['symbol']} | {row['quantity']} | {row['price']} | {row['total_value']}\n"
                    )
                file.write(f"Total Value | {total_value}\n")
        else:
            with open(filename, "w", newline="", encoding="utf-8") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(["Stock", "Quantity", "Price", "Total Value"])
                for row in rows:
                    writer.writerow([row["symbol"], row["quantity"], row["price"], row["total_value"]])
                writer.writerow(["Total", "", "", total_value])

        print(f"Results saved to {filename}")
        return


def main():
    """Run the full stock portfolio tracker program."""
    print("Welcome to the Stock Portfolio Tracker!")
    holdings = get_user_input()

    if not holdings:
        print("No holdings entered. Exiting program.")
        return

    rows, total_value = calculate_totals(holdings)
    display_summary(rows, total_value)
    save_to_file(rows, total_value)


if __name__ == "__main__":
    main()
