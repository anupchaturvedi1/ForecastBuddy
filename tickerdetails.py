import csv

def get_ticker():
   """Reads a CSV file and returns a list of ticker values."""
   file_path = 'tickerlist.csv'
   with open(file_path, 'r') as file:
        reader = csv.reader(file)
        ticket_list = []

        for row in reader:
            ticket_list.extend(row)
   return ticket_list


