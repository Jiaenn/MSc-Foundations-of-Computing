from matplotlib import pyplot as plt, ticker
import numpy as np
import csv
from PartB import creat_portfolio


def plot_company(data, code, start_date, end_date):
    diff = int(end_date[:2]) - int(start_date[:2]) + 1
    price = []
    x_time = []
    y_price = []

    i = 0
    while i < diff:
        for items in data:
            if items['code'] == code:
                if int(items['date'][:2]) == int(start_date[:2]) + i:
                    x_time.append(items['date'][:5] + ' ' + items['time'])
                    y_price.append(round(float(items['price']), 2))
        i += 1

    plt.plot(x_time, y_price, label=code)
    plt.legend(loc='best')

    plt.title("Stock Price Movement")
    plt.xlabel('Time Period')
    plt.ylabel('Price Movement')

    # Set the density of x_axis and y_axis
    if int(end_date[:2]) - int(start_date[:2]) <= 2:
        x_ticker = 10
        y_ticker = 1

    else:
        x_ticker = 10
        y_ticker = 3

    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(x_ticker))
    plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(y_ticker))

    plt.xticks(rotation=45)

    plt.tight_layout()
    icon_path = "E:\Postgraduate - University of Warwick\CS917 Foundations of Computing\Coursework1"
    save_fig1 = plt.savefig('plot1.png'.format(icon_path))

    plt.show()

    return save_fig1


def plot_portfolio(data, portfolio, start_date, end_date):
    diff = int(end_date[:2]) - int(start_date[:2]) + 1
    price = []
    x_time = []
    y_price = []

    for n in range(len(portfolio)):
        x_time.append([])
        y_price.append([])
        i = 0
        for items in data:
            if items['code'] == portfolio[n] and int(items['date'][:2]) == int(start_date[:2]) + i:
                for i in range(diff):
                    x_time[n].append(items['date'][:5] + ' ' + items['time'])
                    y_price[n].append(round(float(items['price']), 2))
                    i += 1

    for i in range(0, len(portfolio)):
        if len(portfolio) <= 2:
            plt.subplot(1, 2, i + 1)

        elif 2 < len(portfolio) <= 4:
            plt.subplot(2, 2, i + 1)

        else:
            plt.subplot(2, 3, i + 1)

        plt.plot(x_time[i], y_price[i], label=portfolio[i])

        # Set the density of x_axis and y_axis

        plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(10))
        plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(3))

        plt.legend(loc='lower center')

        plt.xlabel('Time Period')
        plt.ylabel('Price Movement')

        plt.xticks(rotation=45)

        plt.suptitle("Stock Price Movement")

    plt.tight_layout()
    icon_path = "E:\Postgraduate - University of Warwick\CS917 Foundations of Computing\Coursework1"
    save_fig2 = plt.savefig('plot2.png'.format(icon_path))

    plt.show()

    return save_fig2


if __name__ == "__main__":
    # Start the program
    data = []
    with open("ftse100.csv", "r") as f:
        reader = csv.DictReader(f)
        data = [r for r in reader]

    code = "SSE"
    start_date = "14/10/2019"
    end_date = "16/10/2019"

    # plot_company(data, code, start_date, end_date)

    portfolio = creat_portfolio(data)
    if len(portfolio) > 6:
        print("Portfolio size is greater than 6, first six company codes are kept.")
        portfolio = portfolio[:6]

    plot_portfolio(data, portfolio, start_date, end_date)

    pass
