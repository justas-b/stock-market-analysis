import requests
import json
from rich.prompt import Prompt
from rich.console import Console
from rich.table import Table

API_KEY = 0 # enter your API key
API_URL = "https://www.alphavantage.co/query?"

console = Console(record = True)

if not API_KEY:
    with open('apikey.txt', 'r') as f:
        API_KEY = f.readline()


def display_basic_company(company):
    stock_table = Table(title="Basic Company Information")
    column_styles = ["blue1", "blue1", "dark_goldenrod", "deep_pink4", "light_steel_blue"]
    table_columns = ["Symbol", "Name", "Type", "Region", "Currency"]

    for index, column in enumerate(table_columns):
        stock_table.add_column(column, style = column_styles[index])

    stock_table.add_row(company["1. symbol"], company["2. name"], company["3. type"], company["4. region"], company["8. currency"])
    console.print(stock_table)


def display_detailed_company(company):
    symbol = company["1. symbol"]
    stock_table = Table(title="Company Information")
    column_styles = ["blue1", "blue1", "dark_goldenrod", "deep_pink4", "light_steel_blue", "green4", "red", "green_yellow"]
    table_columns = ["Symbol", "Name", "Exchange", "Country", "Sector", "Year High", "Year Low", "Divident/Share"]

    response = requests.get(API_URL + f"function=OVERVIEW&symbol={symbol}&apikey={API_KEY}")
    detailed_company = response.json()

    if detailed_company:
        for index, column in enumerate(table_columns):
            stock_table.add_column(column, style = column_styles[index])

        stock_table.add_row(detailed_company["Symbol"], detailed_company["Name"], detailed_company["Exchange"], detailed_company["Country"], detailed_company["Sector"], detailed_company["52WeekHigh"], detailed_company["52WeekLow"], detailed_company["DividendPerShare"])
        console.print(stock_table)
    else:
        display_basic_company(company)


def stock_search(term):
    response = requests.get(API_URL + f"function=SYMBOL_SEARCH&keywords={term}&apikey={API_KEY}")
    matches = response.json()['bestMatches']

    if len(matches):
        if len(matches) == 1:
            return matches[0]
        else:
            matches_list = []
            for match in matches:
                matches_list.append(match["1. symbol"])
            
            user_choice = Prompt.ask("Please choose out of the following tickers", choices =matches_list)
            return [match for match in matches if match["1. symbol"] == user_choice][0]
    else:
        console.print(f"{term} not found!")
        return 0


def month_analysis(symbol):
    response = requests.get(API_URL + f"function=TIME_SERIES_MONTHLY&symbol={symbol}&apikey={API_KEY}")
    records = response.json()["Monthly Time Series"]

    month_table = Table(title = f"{symbol} Monthly Stock Price")
    column_styles = ["blue3", "bright_red", "bright_green", "bright_magenta", "bright_red"]
    table_columns = ["Date", "Open Price", "Close Price", "Price Difference", "Percentage Change"]

    for index, column in enumerate(table_columns):
        month_table.add_column(column, style = column_styles[index])

    for date in records:
        open_price = float(records[date]["1. open"])
        close_price = float(records[date]["4. close"])
        price_difference = round(close_price - open_price, 2)
        percentage_change = round(price_difference / open_price, 2)
        month_table.add_row(date, str(open_price), str(close_price), str(price_difference), str(percentage_change))
    
    console.print(month_table)


def display_information(user_input, stock):
    match user_input:
        case "Company Information":
            return display_detailed_company(stock)
        case "Monthly Performance":
            return month_analysis(stock["1. symbol"])


if __name__ == "__main__":
    stock_input = Prompt.ask("Please search for a stock")
    stock = stock_search(stock_input)

    while not stock:
        stock_input = Prompt.ask("Please search for a stock")
        stock = stock_search(stock_input)

    user_input = Prompt.ask("Please choose what information you would like displayed: ", choices=["Company Information", "Monthly Performance"])
    display_information(user_input, stock)

