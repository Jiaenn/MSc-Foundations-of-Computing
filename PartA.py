import csv


def daily_movement(data, code, date):
    open_price = 0
    close_price = 0

    for items in data:
        if items['code'] == code and items['date'] == date and items['time'] == "09:00":
            open_price = float(items['price'])

        if items['code'] == code and items['date'] == date and items['time'] == "17:00":
            close_price = float(items['price'])

    daily_move = close_price - open_price

    return daily_move, open_price, close_price


def daily_high(data, code, date):
    price = []

    for items in data:
        if items['code'] == code and items['date'] == date:
            price.append(items['price'])

    price_highest = float(price[0])

    for high in price:
        if float(high) > price_highest:
            price_highest = float(high)

    return price, price_highest


def daily_low(data, code, date):
    price = daily_high(data, code, date)[0]

    price_lowest = float(price[0])

    for low in price:
        if float(low) < price_lowest:
            price_lowest = float(low)

    return price_lowest


# daily_avg(data, code, date) -> float
def daily_avg(data, code, date):
    price = daily_high(data, code, date)[0]
    total = 0.00  # Sum up the prices in a day

    for n in range(len(price)):
        total += float(price[n])
        n += 1
    avg = total / len(price)

    return avg


# percentage_change(data, code, date) -> float
def percentage_change(data, code, date):

    price_movement = daily_movement(data, code, date)[0]
    open_price = daily_movement(data, code, date)[1]

    change = price_movement / open_price

    return change


# Define a function to round up the digits, use when two decimals are required to be kept
def round_up(value):
    return round(value*100) / 100.0


# Replace the body of this main function for your testing purposes
if __name__ == "__main__":
    # Start the program

    # Example variable initialization
    # data is always the ftse100.csv read in using a DictReader
    data = []
    with open("ftse100.csv", "r") as f:
        reader = csv.DictReader(f)
        data = [r for r in reader]

    code = 'UU.'
    date = '16/10/2019'

    movement = daily_movement(data, code, date)[0]
    print("Daily_movement of", code, "on", date, "is:", "%.2f" % round_up(movement))

    highest = daily_high(data, code, date)[1]
    print("The highest price of", code, "on", date, "is:", "%.2f" % round_up(highest))

    lowest = daily_low(data, code, date)
    print("The lowest price of", code, "on", date, "is:", "%.2f" % round_up(lowest))

    average = daily_avg(data, code, date)
    print("The average price of", code, "on", date, "is:", "%.2f" % round_up(average))

    per_change = percentage_change(data, code, date)
    print("Percentage change of", code, "on", date, "is:", "{:.2%}".format(round_up(per_change)))
    pass
