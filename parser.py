import csv
import json
import os

#file import
from figi import *
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
    isin_seen = set()
    
    #Does a first iteration because the algorithm needs to fetch
    # the tickers first. Only then can it start to calculate all the metrics
    with open(FILENAME) as csvfile:
        jobs = []
        for idx,row in enumerate(csv.DictReader(csvfile)):
            degiro.history = [row] + degiro.history
            #Parses the ISIN and gets the ticker of the company 
            if row['ISIN'] != '' and row['ISIN'] not in isin_seen:
                jobs.append({'idType': 'ID_ISIN', 'idValue': row['ISIN'], 'exchCode': 'US'})
                isin_seen.add(row['ISIN'])
                #openfigi supports a maximum of 100 jobs per request
                if len(jobs) >= 100:
                    ticker_info = [_['data'][0] for _ in OpenFIGI.map_jobs(jobs) if 'error' not in _]
                    ticker_info = { e['ticker']:{'realized_profit':0,'num_shares':0} for e in ticker_info}
                    jobs.clear()
                    degiro.tickers.update(ticker_info)
        if len(jobs) > 0:
            ticker_info = [_['data'][0] for _ in OpenFIGI.map_jobs(jobs) if 'error' not in _]
            ticker_info = { e['ticker']:{'realized_profit':0,'num_shares':0} for e in ticker_info}
            jobs.clear()
            degiro.tickers.update(ticker_info)

    
    #TODO: REMOVE LATER
    with open('output_tickers.json', 'w') as outfile1:
        json.dump(degiro.tickers, outfile1, indent=4)
    
    with open('output_history.json', 'w') as outfile2:
        json.dump(degiro.history, outfile2, indent=4)

    # for transaction in degiro.history:
        
    #     description = transaction['Descrição']
    #     if is_share_sell(description) or is_share_buy(description): #is a buy/sell transaction
    #         print(description)


if __name__=='__main__':
    main()