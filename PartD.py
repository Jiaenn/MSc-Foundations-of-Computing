import matplotlib.pyplot as plt
import csv
import numpy as np
from PartA import*


class Company:
    def __init__(self, code, name, currency, date):
        self.code = code
        self.name = name
        self.currency = currency
        self.date = date

    def daily_movement(self, data):
        open_price = 0
        close_price = 0
        price_movement = 0

        for items in data:
            if items['code'] == self.code and items['date'] == self.date and items['time'] == "09:00":
                open_price = float(items['price'])

            if items['code'] == self.code and items['date'] == self.date and items['time'] == "17:00":
                close_price = float(items['price'])

        price_movement = open_price - close_price

        return price_movement, open_price, close_price

    def daily_high(self, data):
        price = []

        for items in data:
            if items['code'] == self.code and items['date'] == self.date:
                price.append(items['price'])

        price_highest = float(price[0])

        for high in price:
            if float(high) > price_highest:
                price_highest = float(high)

        return price, price_highest

    def daily_low(self, data):
        price = Company.daily_high(self, data)[0]

        price_lowest = float(price[0])

        for low in price:
            if float(low) < price_lowest:
                price_lowest = float(low)

        return price_lowest

    def daily_avg(self, data):
        price = self.daily_high(data)[0]
        total = 0.00  # Sum up the prices in a day
        avg = 0.00

        for n in range(len(price)):
            total += float(price[n])
            n += 1
        avg = total / len(price)

        return float(avg)

    def percentage_change(self, data):
        per_change = 0.00

        price_movement = self.daily_movement(data)[0]
        open_price = self.daily_movement(data)[1]

        per_change = price_movement / open_price

        return per_change

    pass


def regression(x, y, x_predict):
    # Calculate the mean of x and y separately
    x_mean = float(np.mean(x))
    y_mean = float(np.mean(y))

    # Calculate the numerator and denominator according to the formula
    numerator = 0.00
    denominator = 0.00
    for x_i, y_i in zip(x, y):
        numerator += ((float(x_i) - float(x_mean)) * (float(y_i) - float(y_mean)))
        denominator += (int(float(x_i) - float(x_mean)) ** 2)

    # Calculate the coefficient of x as well as the intercept for the regression model
    m = "% .2f" % round_up(float(numerator) / float(denominator))
    b = "% .2f" % round_up(float(y_mean) - (float(m) * float(x_mean)))

    y_predict = float(m) * float(x_predict) + float(b)

    return y_predict


# predict_next_average(company) -> float
def predict_next_average(company):
    x_date = []
    y_avg = []

    # Extract the average price on each date
    for items in data:
        if items['code'] == company.code and items['time'] == "09:00":
            company.date = items['date']

            x_date.append(company.date)
            y_avg.append(company.daily_avg(data))

    # Change date into numeric constants in range [0,4]
    n = 0
    for i in x_date:
        x_date[n] = n
        n += 1

    # Calculate the predicted average price on next Monday
    y_predict = regression(x_date, y_avg, x_predict=5.00)

    return y_predict


# classify_trend(company) -> str
def classify_trend(company):
    x_date = []
    y_high = []
    y_low = []

    # Extract the daily_high and daily_low on each date
    for items in data:
        if items['code'] == company.code and items['time'] == "09:00":
            company.date = items['date']

            x_date.append(company.date)
            y_high.append(float(company.daily_high(data)[1]))
            y_low.append(float(company.daily_low(data)))

    # Change date into numeric constants in range [0,4]
    n = 0
    for i in x_date:
        x_date[n] = n
        n += 1

    # Calculate the predicted price for daily_high and daily_low on next Monday
    y_predict_high = regression(x_date, y_high, x_predict=5.00)
    y_predict_low = regression(x_date, y_low, x_predict=5.00)

    # Find out the daily_high and daily_low last Friday
    company.date = "18/10/2019"
    last_daily_high = company.daily_high(data)[1]
    last_daily_low = company.daily_low(data)

    # Calculate the difference of daily high between true value and predicted value
    trend_high = y_predict_high - last_daily_high
    trend_low = y_predict_low - last_daily_low

    # Classify the trend
    if trend_high > 0 and trend_low < 0:
        trend = "Trend: volatile"

    elif trend_high > 0 and trend_low > 0:
        trend = "Trend: increasing"

    elif trend_high < 0 and trend_low < 0:
        trend = "Trend: decreasing"
    else:
        trend = "Trend: other"

    print(trend)

    return trend


# Replace the body of this main function for your testing purposes
if __name__ == "__main__":
    # Start the program
    data = []
    with open("ftse100.csv", "r") as f:
        reader = csv.DictReader(f)
        data = [r for r in reader]

    print("Part A:")
    c = Company('UU.', 'UTD. UTILITIES', 'GBX', "14/10/2019")

    price_move = c.daily_movement(data)[0]
    print("Daily_movement of", c.code, "on", c.date, "is:", "%.2f" % round_up(price_move))

    price_high = c.daily_high(data)[1]
    print("Highest price of", c.code, "on", c.date, "is:", "%.2f" % round_up(price_high))

    price_low = c.daily_low(data)
    print("Lowest price of", c.code, "on", c.date, "is:", "%.2f" % round_up(price_low))

    daily_average = c.daily_avg(data)
    print("Average price of", c.code, "on", c.date, "is:", "%.2f" % round_up(daily_average))

    percentage_change = c.percentage_change(data)
    print("Percentage change of", c.code, "on", c.date, "is:", "{:.2%}".format(round_up(percentage_change)), "\n")

    print("Part B:")
    y_predicted = predict_next_average(c)
    print("Predicted price on next Monday is:", "% .2f" % round_up(y_predicted))

    classify_trend(c)

    pass
