import os

#file import
from degiro import *

FILENAME = 'dataset/account.csv'

def main():

    degiro = Degiro()
    #load from file
    degiro.load_file(FILENAME)
    # queries
    result = degiro.query(
        query_type=TransactionType.DEGIRO_TRANSACTION_COMISSION,
        #end_date=datetime.strptime('31-12-1998 23:23:00', '%d-%m-%Y %H:%M:%S'),
        start_date=datetime.strptime('31-12-2020 23:59:00', '%d-%m-%Y %H:%M:%S')
    )
    print(result)

    #dumping data structures        
    with open('output_transactions.json', 'w') as outfile2:
        json.dump(degiro.transactions, outfile2, indent=4)

    with open('result.json', 'w') as outfile:
        json.dump(result, outfile, indent=4)

if __name__=='__main__':
    main()