import csv
import json
from enum  import Enum
from datetime import datetime


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
        self.connectivity_costs = []
        self.comissions = []
        # auxiliar variables
        self.__jobs = []
        self.__currency_exchange = None

    def get_ticker_info(self):
        ticker_info = [_['data'][0] for _ in OpenFIGI.map_jobs(self.__jobs) if 'error' not in _]
        ticker_info = { e['ticker']:{'realized_profit':0,'num_shares':0} for e in ticker_info}
        self.__jobs.clear()
        self.tickers.update(ticker_info)

    def create_history(self,filename):
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

    def load_file(self,filename):

        self.create_history(filename)

        for transaction in self.history:

            trans = self.get_transaction_info(transaction)
            if trans:
                trans_date = datetime.strptime(trans['date'], '%d-%m-%Y %H:%M:%S')
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
                
                elif trans['type'] == Degiro.TransactionType.DEGIRO_TRANSACTION_COMISSION:
                    query_date = datetime.strptime('31-12-2020 23:59:59','%d-%m-%Y %H:%M:%S')
                    self.comissions.append(trans)
                
                elif trans['type'] == Degiro.TransactionType.DEGIRO_CONNECTIVITY_COST:
                    self.connectivity_costs.append(trans)        
            

    def get_transaction_info(self,transaction):
        description = transaction['Descrição']
        date = '%s %s:00' % (transaction['Data'],transaction['Hora'])
        if transaction['Montante'] != '':
            transaction['Montante'] = float(transaction['Montante'].replace(',','.'))

            if  description == 'Flatex Cash Sweep Transfer' or description == 'Degiro Cash Sweep Transfer':
                return {
                    'type': Degiro.TransactionType.DEGIRO_CASH_SWEEP,
                    'date': date,
                    'currency': transaction['Mudança'],
                    'amount':transaction['Montante']
                }

            # When the new currency is credited to the account
            elif description == 'Crédito de divisa':
                return {
                    'type': Degiro.TransactionType.CURRENCY_EXCHANGE_CREDIT,
                    'date': date,
                    'currency': transaction['Mudança'],
                    'amount':transaction['Montante']
                }

            #When the old currency is deducted from the account
            elif description == 'Levantamento de divisa':
                return {
                    'type': Degiro.TransactionType.CURRENCY_EXCHANGE_DEDUCTION,
                    'date': date,
                    'currency': transaction['Mudança'],
                    'amount':transaction['Montante']
                }

            # Tracks degiro's commissions
            elif description == 'Comissão de transação':
                return {
                    'type': Degiro.TransactionType.DEGIRO_TRANSACTION_COMISSION,
                    'date': date,
                    'currency': transaction['Mudança'],
                    'amount':transaction['Montante']
                }
            
            # degiro's commission for connecting to the stock exchanges
            elif 'Custo de Conectividade' in description:
                return {
                    'type': Degiro.TransactionType.DEGIRO_CONNECTIVITY_COST,
                    'date': date,
                    'currency': transaction['Mudança'],
                    'amount':transaction['Montante'],
                    'exchange': description[description.find("(")+1:description.find(")")]
                }
    

