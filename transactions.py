from enum  import Enum
import json

class Transaction:
    def __init__(self,t,d):
        self.type = t
        self.date = d

class TransactionBuyShares(Transaction,dict):
    def __init__(self,tdate,tshares,tprice,tticker):
        super().__init__(TransactionType.BUY_SHARES,tdate)
        self.shares = tshares
        self.pps = tprice #price per share
        self.ticker = tticker
        dict.__init__(self, self.__dict__)

class TransactionSellShares(Transaction,dict):
    def __init__(self,tdate,tshares,tprice,tticker):
        super().__init__(TransactionType.SELL_SHARES,tdate)
        self.shares = tshares
        self.pps = tprice #price per share
        self.ticker = tticker
        dict.__init__(self, self.__dict__)

class TransactionType(int, Enum):
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