import requests
import json
from rich.prompt import Prompt
from rich.console import Console
from rich.table import Table

# API_KEY = "YOUR_KEY"
API_URL = "https://www.alphavantage.co/query?"

console = Console(record = True)


def display_stock(stock):
    stock_table = Table(title="Stock Information")
    table_columns = ["Symbol", "Name", "Type", "Region", "Currency"]

    for column in table_columns:
        stock_table.add_column(column)

    stock_table.add_row(stock["1. symbol"], stock["2. name"], stock["3. type"], stock["4. region"], stock["8. currency"])

    console.print(stock_table)


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
            
            user_choice = Prompt.ask("Please choose out of the following tickers", choices=matches_list)
            return [match for match in matches if match["1. symbol"] == user_choice][0]
    else:
        return f"No matches for {term} found!" 



if __name__ == "__main__":
    stock_input = Prompt.ask("Please search for a stock: ")
    stock = stock_search(stock_input)
    display_stock(stock)