import csv
import os
import requests


# def get_ticker():
#    """Reads a CSV file and returns a list of ticker values."""
#    file_path = 'tickerlist.csv'
#    with open(file_path, 'r') as file:
#         reader = csv.reader(file)
#         ticket_list = []

#         for row in reader:
#             ticket_list.extend(row)
#    return ticket_list

def get_ticker():
    api_key = os.environ.get("FMPCLOUD_API_KEY")
    
    print("test" + api_key)
    
    api_url = "https://fmpcloud.io/api/v3/stock/list?apikey=" + api_key

    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        print(data)
        if data:
            field_values = [item['symbol'] for item in data if item['exchangeShortName'] == 'NASDAQ']
            print(field_values)
        else:
            field_values = []
        return field_values
    else:
        return None        

