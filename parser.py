import os

#file import
from degiro import *

FILENAME = 'dataset/account.csv'


# jobs = [
#     {'idType': 'ID_ISIN', 'idValue': 'US36467W1099', 'exchCode': 'US'},#gamestop
#     {'idType': 'ID_ISIN', 'idValue': 'CA09228F1036', 'exchCode': 'US'},#blackberry
#     {'idType': 'ID_ISIN', 'idValue': 'US0079031078', 'exchCode': 'US'},#amd
#     {'idType': 'ID_ISIN', 'idValue': 'US6549022043', 'exchCode': 'US'},#nokia
#     {'idType': 'ID_ISIN', 'idValue': 'US69608A1088', 'exchCode': 'US'},#palantir
#     {'idType': 'ID_ISIN', 'idValue': 'US5949181045', 'exchCode': 'US'},#microsoft
#     {'idType': 'ID_ISIN', 'idValue': 'US30303M1027', 'exchCode': 'US'},#facebook
#     {'idType': 'ID_ISIN', 'idValue': 'BMG491BT1088', 'exchCode': 'US'},#ivz
#     {'idType': 'ID_ISIN', 'idValue': 'US46131B1008', 'exchCode': 'US'},#ivr
#     {'idType': 'ID_ISIN', 'idValue': 'US2546871060', 'exchCode': 'US'},#dis
#     {'idType': 'ID_ISIN', 'idValue': 'IL0011582033', 'exchCode': 'US'},#fvrr
#     {'idType': 'ID_ISIN', 'idValue': 'PA1436583006', 'exchCode': 'US'},#ccl
#     {'idType': 'ID_ISIN', 'idValue': 'US0258161092', 'exchCode': 'US'},#axp
#     {'idType': 'ID_ISIN', 'idValue': 'US4781601046', 'exchCode': 'US'},#jnj
# ]


def main():

    degiro = Degiro()
    #load from file
    degiro.load_file(FILENAME)
    # queries
    with open('output_exchanges.json', 'w') as outfile1:
        json.dump(degiro.exchanges, outfile1, indent=4)
        
    with open('output_tickers.json', 'w') as outfile2:
        json.dump(degiro.tickers, outfile2, indent=4)
    
    with open('output_history.json', 'w') as outfile3:
        json.dump(degiro.history, outfile3, indent=4)

    with open('output_connectivity_costs.json', 'w') as outfile4:
        for elem in degiro.connectivity_costs:
            del elem['type']
        json.dump(degiro.connectivity_costs, outfile4, indent=4)

    with open('output_comissions.json', 'w') as outfile5:
        for elem in degiro.comissions:
            del elem['type']
        json.dump(degiro.comissions, outfile5, indent=4)

if __name__=='__main__':
    main()