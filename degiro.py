import csv
import json
import re
from datetime import datetime

#file imports
from figi import *
from transactions import *

class Degiro:

    def __init__(self):
        self.transactions = []
        self.connectivity_costs = []
        self.comissions = []
        # auxiliar variables
        self.__isin_ticker = {}
        self.__jobs = []
        self.__currency_exchange = None
        self.__history = []


    '''
    Public methods
    '''
    #queries the existing information
    def query(self,query_type,end_date=datetime.now(),start_date=None):
        if not start_date:
            start_date = datetime.utcfromtimestamp(0)

        print('Searching transactions of type %d from %s to %s...'%(query_type,str(start_date),str(end_date)))
        result = []
        for trans in self.transactions:
            trans_date = datetime.strptime(trans['date'], '%d-%m-%Y %H:%M:%S')
            if query_type == trans['type'] and start_date <= trans_date and trans_date <= end_date:
                result.append(trans)

        return result

    def load_file(self,filename):

        self.create_history(filename)

        exchange_aux = None
        for transaction in self.__history:

            trans = self.get_transaction_info(transaction)
            if trans:
                if trans.type == TransactionType.CURRENCY_EXCHANGE_OUTFLOW:
                    if not exchange_aux:
                        exchange_aux = trans
                    else:
                        self.transactions.append(
                            TransactionExchange(
                                trans.date,
                                exchange_aux.currency,
                                exchange_aux.amount,
                                trans.currency,
                                trans.amount
                            )
                        )
                        exchange_aux = None
                
                elif trans.type == TransactionType.CURRENCY_EXCHANGE_INFLOW:
                    if not exchange_aux:
                        exchange_aux = trans
                    else:
                        self.transactions.append(
                            TransactionExchange(
                                trans.date,
                                trans.currency,
                                trans.amount,
                                exchange_aux.currency,
                                exchange_aux.amount
                            )
                        )
                        exchange_aux = None
                else:
                    self.transactions.append(trans)


    '''
    Private methods
    '''
    def get_ticker_info(self):
        raw = OpenFIGI.map_jobs(self.__jobs)
        i = 0
        for k in raw:
            if 'error' not in k:
                self.__isin_ticker[self.__jobs[i]['idValue']] = k['data'][0]['ticker']
            i += 1
        self.__jobs.clear()

    def create_history(self,filename):
        isin_seen = set()
        #Does a first iteration because the algorithm needs to fetch
        # the tickers first. Only then can it start to calculate all the metrics
        with open(filename) as csvfile:
            self.__jobs = []
            for idx,row in enumerate(csv.DictReader(csvfile)):
                self.__history = self.__history + [row]
                #Parses the ISIN and gets the ticker of the company 
                if row['ISIN'] != '' and row['ISIN'] not in isin_seen:
                    self.__jobs.append({'idType': 'ID_ISIN', 'idValue': row['ISIN'], 'exchCode': 'US'})
                    isin_seen.add(row['ISIN'])
                    #openfigi supports a maximum of 100 jobs per request
                    if len(self.__jobs) >= 100:
                        self.get_ticker_info()
            if len(self.__jobs) > 0:
                self.get_ticker_info()  

    def get_transaction_info(self,transaction):
        description = transaction['Descrição']
        date = '%s %s:00' % (transaction['Data'],transaction['Hora'])
        if transaction['Montante'] != '':
            transaction['Montante'] = float(transaction['Montante'].replace(',','.'))

            if  description == 'Flatex Cash Sweep Transfer' or\
                description == 'Degiro Cash Sweep Transfer':
                return TransactionCashSweep(
                    tdate=date,
                    tcurrency=transaction['Mudança'],
                    tamount=transaction['Montante'],
                )

            # When the new currency is credited to the account
            if description == 'Crédito de divisa':
                return TransactionExchangeOutflow(
                    tdate=date,
                    tcurrency=transaction['Mudança'],
                    tamount=transaction['Montante'],
                )

            #When the old currency is deducted from the account
            if description == 'Levantamento de divisa':
                return TransactionExchangeInflow(
                    tdate=date,
                    tcurrency=transaction['Mudança'],
                    tamount=transaction['Montante'],
                )

            # Tracks degiro's commissions
            if description == 'Comissão de transação':
                return TransactionComission(
                    tdate=date,
                    tcurrency=transaction['Mudança'],
                    tamount=transaction['Montante'],
                )
            
            # degiro's commission for connecting to the stock exchanges
            if 'Custo de Conectividade' in description:
                return TransactionConnectivityCost(
                    tdate=date,
                    tcurrency=transaction['Mudança'],
                    tamount=transaction['Montante'],
                    texchange=description[description.find("(")+1:description.find(")")]
                )

            if 'deposit' in description.lower() or 'depósito' in description.lower():
                return Deposit(
                    tdate=date,
                    tcurrency=transaction['Mudança'],
                    tamount=transaction['Montante']
                )

            # Buying shares transaction
            isin = description[description.rfind("(")+1:description.rfind(")")]
            lst = re.compile('Compra (.*)@(.*) USD').findall(description)
            if len(lst) > 0: #it's a buy transaction
                lst = lst[0]
                info = lst[0].split()
                return TransactionBuyShares(
                    tdate=date,
                    tshares=int(info[0]),
                    tprice=float(lst[1].replace(',','.')),
                    tticker=self.__isin_ticker[isin]
                )
    
            # Selling shares transaction
            lst = re.compile('Venda (.*)@(.*) USD').findall(description)
            if len(lst) > 0: #it's a sell transaction
                lst = lst[0]
                info = lst[0].split()
                return TransactionSellShares(
                    tdate=date,
                    tshares=int(info[0]),
                    tprice=float(lst[1].replace(',','.')),
                    tticker=self.__isin_ticker[isin]
                )
