import csv
import json
from enum  import Enum

#file imports
from figi import *

class Degiro:

    class TransactionType(Enum):
        SELL_SHARES = 1 # Venda x FACEBOOK@300
        BUY_SHARES = 2 # Compra x FACEBOOK@200
        FLATEX_INTEREST = 3 #Flatex Interest
        FLATEX_INTEREST_INCOME = 4 #Flatex Interest Income
        CURRENCY_EXCHANGE_DEDUCTION = 5 # Levantamento de divisa | Crédito de divisa
        CURRENCY_EXCHANGE_CREDIT = 6 # Levantamento de divisa | Crédito de divisa
        DEGIRO_TRANSACTION_COMISSION = 7 # Comissão de transação
        DEGIRO_CONNECTIVITY_COST = 8 #Custo de Conectividade DEGIRO 2021 
        DEGIRO_CASH_SWEEP = 9 #Degiro Cash Sweep Transfer | #Flatex Cash Sweep Transfer
        DEPOSIT = 10 #flatex Deposit
        WITHDRAWAL = 11 #Withdrawal
        DIVIDEND = 12 # Dividendo
        DIVIDEND_TAX = 13 #Imposto sobre dividendo

    def __init__(self):
        self.history = []
        self.tickers = {}
        self.exchanges = []
        # auxiliar variables
        self.__jobs = []
        self.__currency_exchange = None

    def get_ticker_info(self):
        ticker_info = [_['data'][0] for _ in OpenFIGI.map_jobs(self.__jobs) if 'error' not in _]
        ticker_info = { e['ticker']:{'realized_profit':0,'num_shares':0} for e in ticker_info}
        self.__jobs.clear()
        self.tickers.update(ticker_info)

    def load_file(self,filename):
        isin_seen = set()
        #Does a first iteration because the algorithm needs to fetch
        # the tickers first. Only then can it start to calculate all the metrics
        with open(filename) as csvfile:
            self.__jobs = []
            for idx,row in enumerate(csv.DictReader(csvfile)):
                self.history = self.history + [row]
                #Parses the ISIN and gets the ticker of the company 
                if row['ISIN'] != '' and row['ISIN'] not in isin_seen:
                    self.__jobs.append({'idType': 'ID_ISIN', 'idValue': row['ISIN'], 'exchCode': 'US'})
                    isin_seen.add(row['ISIN'])
                    #openfigi supports a maximum of 100 jobs per request
                    if len(self.__jobs) >= 100:
                        self.get_ticker_info()
            if len(self.__jobs) > 0:
                self.get_ticker_info()

        
        #####TODO: REMOVE LATER############
        with open('output_tickers.json', 'w') as outfile1:
            json.dump(self.tickers, outfile1, indent=4)
        
        with open('output_history.json', 'w') as outfile2:
            json.dump(self.history, outfile2, indent=4)
        #################################

        comissions = 0
        for transaction in self.history:

            trans = self.get_transaction_info(transaction)
            print(trans)
            if trans:
                if trans['type'] == Degiro.TransactionType.CURRENCY_EXCHANGE_CREDIT:
                    if self.__currency_exchange:
                        self.exchanges.append({
                            'date': trans['date'],
                            'start_currency': self.__currency_exchange['currency'],
                            'start_amount':self.__currency_exchange['amount'],
                            'target_currency': trans['currency'],
                            'target_amount':trans['amount']
                        })
                        self.__currency_exchange = None
                    else:
                        self.__currency_exchange = trans

                elif trans['type'] == Degiro.TransactionType.CURRENCY_EXCHANGE_DEDUCTION:
                    if self.__currency_exchange:
                        self.exchanges.append({
                            'date': trans['date'],
                            'start_currency': trans['currency'],
                            'start_amount':trans['amount'],
                            'target_currency': self.__currency_exchange['currency'],
                            'target_amount':self.__currency_exchange['amount']
                        })
                        self.__currency_exchange = None
                    else:
                        self.__currency_exchange = trans
        
        with open('output_exchanges.json', 'w') as outfile1:
            json.dump(self.exchanges, outfile1, indent=4)
        #print('Exchanges',self.exchanges)

    def get_transaction_info(self,transaction):
        description = transaction['Descrição']
        if transaction['Montante'] != '':
            if  description == 'Flatex Cash Sweep Transfer' or description == 'Degiro Cash Sweep Transfer':
                return {
                    'type': Degiro.TransactionType.DEGIRO_CASH_SWEEP,
                    'date': '%s %s' % (transaction['Data'],transaction['Hora']),
                    'currency': transaction['Mudança'],
                    'amount':transaction['Montante']
                }

            # When the new currency is credited to the account
            elif description == 'Crédito de divisa':
                return {
                    'type': Degiro.TransactionType.CURRENCY_EXCHANGE_CREDIT,
                    'date': '%s %s' % (transaction['Data'],transaction['Hora']),
                    'currency': transaction['Mudança'],
                    'amount':transaction['Montante']
                }

            #When the old currency is deducted from the account
            elif description == 'Levantamento de divisa':
                return {
                    'type': Degiro.TransactionType.CURRENCY_EXCHANGE_DEDUCTION,
                    'date': '%s %s' % (transaction['Data'],transaction['Hora']),
                    'currency': transaction['Mudança'],
                    'amount':transaction['Montante']
                }

            # Tracks degiro's commissions
            elif description == 'Comissão de transação':
                return {
                    'type': Degiro.TransactionType.DEGIRO_TRANSACTION_COMISSION,
                    'date': '%s %s' % (transaction['Data'],transaction['Hora']),
                    'currency': transaction['Mudança'],
                    'amount':transaction['Montante']
                }
        


