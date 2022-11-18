import requests
import json
from rich.prompt import Prompt
from rich.console import Console
from rich.table import Table

# API_KEY = "your_api_key"
API_URL = "https://www.alphavantage.co/query?"

console = Console(record = True)

def stock_search(term):
    response = requests.get(API_URL + f"function=SYMBOL_SEARCH&keywords={term}&apikey={API_KEY}")
    return response.json()['bestMatches']


if __name__ == "__main__":
    stock_search = Prompt.ask("Please search for a stock: ")
    console.print(stock_search(stock_search))