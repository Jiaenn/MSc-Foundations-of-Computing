import csv
from PartA import*


def creat_portfolio(data):
    # Creat a list which contains 100 company code, in order to ensure whether the user input the correct .
    company_code = []

    for items in data[:101]:
        company_code.append(items['code'])

    portfolio_list = []

    while True:
        portfolio_list.append(input("Please enter the company code to create a portfolio and input 'Exit' to exit (at "
                                    "least 1 and at most 100 code): "))

        if len(portfolio_list) > 100:
            print("Length of the portfolio is greater than 100.")
            portfolio_list.pop()
            break

        if portfolio_list[-1] in portfolio_list[:-1]:
            print("Code duplicated.")
            portfolio_list.pop()

        if portfolio_list[-1] not in company_code:
            if portfolio_list[0] == 'Exit':
                print("You should input company code for the portfolio.")
                portfolio_list.pop()

            elif portfolio_list[-1] == "Exit":
                portfolio_list.pop()
                break
            else:
                print("Wrong company code.")
                portfolio_list.pop()

    print("Here are your inputs:", portfolio_list)

    return portfolio_list


def best_investments(data, portfolio, x, start_date, end_date):
    i = 0
    portfolio_movement = []

    while i < len(portfolio):
        start_date_price = daily_movement(data, portfolio[i], start_date)[1]
        end_date_price = daily_movement(data, portfolio[i], end_date)[2]
        price_movement = end_date_price - start_date_price
        portfolio_movement.append((portfolio[i], "%.2f" % round_up(price_movement)))
        i += 1

    sorted_movement_best = sorted(portfolio_movement, key=lambda tup: float(tup[1]), reverse=True)[:int(x)]

    return portfolio_movement, sorted_movement_best


def worst_investments(data, portfolio, x, start_date, end_date):
    portfolio_movement = best_investments(data, portfolio, x, start_date, end_date)[0]

    sorted_movement_worst = sorted(portfolio_movement, key=lambda tup: float(tup[:][1]), reverse=False)[:int(x)]

    return sorted_movement_worst


if __name__ == "__main__":
    # Start the program
    data = []
    with open("ftse100.csv", "r") as f:
        reader = csv.DictReader(f)
        data = [r for r in reader]

    portfolio = creat_portfolio(data)

    x = input("Enter the number of investments you are interested in: ")
    if int(x) < 1 or int(x) > len(portfolio):
        print('[]')  # Ensure the user input the number in range [1, len(portfolio)]
    else:
        start_date = input("Please input the start date in the format dd/mm/yyyy: ")
        end_date = input("Please input the end date in the format dd/mm/yyyy: ")

        identify_start_date = start_date.split('/')
        identify_end_date = end_date.split('/')

        if start_date[:2].isdigit() == False or start_date[3:5].isdigit() == False or start_date[6:].isdigit() == False \
                or end_date[:2].isdigit() == False or end_date[3:5].isdigit() == False \
                or end_date[6:].isdigit() == False:
            print('[]')  # Ensure the user input integers for dd mm yyyy

        elif start_date[2] != '/' or start_date[5] != '/' or end_date[2] != '/' or end_date[5] != '/':
            print('[]')  # Ensure the user input the correct format for the dates

        elif int(identify_start_date[1]) != 10 or int(identify_end_date[1]) != 10 \
                or int(identify_start_date[2]) != 2019 or int(identify_end_date[2]) != 2019:
            print('[]')  # Ensure the user input the correct month and year of the dates

        elif int(identify_start_date[0]) < 14 or int(identify_end_date[0]) < 14 \
                or int(identify_start_date[0]) > 18 or int(identify_end_date[0]) > 18:
            print('[]')  # Ensure the user input the day in range [14, 18]

        elif int(identify_start_date[0]) > int(identify_end_date[0]):
            print('[]')  # Ensure the start_date is less than the end_date

        else:
            best = best_investments(data, portfolio, x, start_date, end_date)[1]
            print("List for best investments:\n", best)

            worst = worst_investments(data, portfolio, x, start_date, end_date)
            print("List for worst investment: \n", worst)
    pass
