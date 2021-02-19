import os
import pprint 
pp = pprint.PrettyPrinter(indent=4)


#file import
from degiro import *

FILENAME = 'dataset/Account.csv'

def main():

    degiro = Degiro()
    #load from file
    degiro.load_file(FILENAME)
    # queries
    #result = degiro.query(
    #    query_type=TransactionType.CURRENCY_EXCHANGE,
    #    start_date=datetime.strptime('31-12-2020 23:59:00', '%d-%m-%Y %H:%M:%S'),
    #    #end_date=datetime.strptime('31-12-1998 23:23:00', '%d-%m-%Y %H:%M:%S')
    #)

    result = degiro.get_positions(open_only=True)
    #print(result)
    print(result['AAPL'].pps)
    pp.pprint(result)

    # with open('result.json', 'w') as outfile:
    #     json.dump(result, outfile, indent=4)

if __name__=='__main__':
    main()