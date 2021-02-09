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
        self.pps = tprice #price per share in euros
        self.ticker = tticker
        dict.__init__(self, self.__dict__)

class TransactionConnectivityCost(Transaction,dict):
    def __init__(self,tdate,tcurrency,tamount,texchange):
        super().__init__(TransactionType.DEGIRO_CONNECTIVITY_COST,tdate)
        self.currency = tcurrency
        self.amount = tamount #in euros
        self.exchange = texchange
        dict.__init__(self, self.__dict__)

class TransactionComission(Transaction,dict):
    def __init__(self,tdate,tcurrency,tamount):
        super().__init__(TransactionType.DEGIRO_TRANSACTION_COMISSION,tdate)
        self.currency = tcurrency
        self.amount = tamount #in euros
        dict.__init__(self, self.__dict__)

class TransactionExchange(Transaction,dict):
    def __init__(self,tdate,tcurrencyin,tamountin,tcurrencyout,tamountout):
        super().__init__(TransactionType.CURRENCY_EXCHANGE,tdate)
        self.currency_in = tcurrencyin
        self.amount_in = tamountin 
        self.currency_out = tcurrencyout
        self.amount_out = tamountout 
        dict.__init__(self, self.__dict__)

class TransactionExchangeInflow(Transaction,dict):
    def __init__(self,tdate,tcurrency,tamount):
        super().__init__(TransactionType.CURRENCY_EXCHANGE_INFLOW,tdate)
        self.currency = tcurrency
        self.amount = tamount #in euros
        dict.__init__(self, self.__dict__)

class TransactionExchangeOutflow(Transaction,dict):
    def __init__(self,tdate,tcurrency,tamount):
        super().__init__(TransactionType.CURRENCY_EXCHANGE_OUTFLOW,tdate)
        self.currency = tcurrency
        self.amount = tamount #in euros
        dict.__init__(self, self.__dict__)

class TransactionCashSweep(Transaction,dict):
    def __init__(self,tdate,tcurrency,tamount):
        super().__init__(TransactionType.DEGIRO_CASH_SWEEP,tdate)
        self.currency = tcurrency
        self.amount = tamount #in euros
        dict.__init__(self, self.__dict__)

class Deposit(Transaction,dict):
    def __init__(self,tdate,tcurrency,tamount):
        super().__init__(TransactionType.DEPOSIT,tdate)
        self.currency = tcurrency
        self.amount = tamount #in euros
        dict.__init__(self, self.__dict__)


class TransactionType(int, Enum):
    SELL_SHARES = 1 # Venda x FACEBOOK@300
    BUY_SHARES = 2 # Compra x FACEBOOK@200
    FLATEX_INTEREST = 3 #Flatex Interest
    FLATEX_INTEREST_INCOME = 4 #Flatex Interest Income
    CURRENCY_EXCHANGE_OUTFLOW = 5 # Levantamento de divisa
    CURRENCY_EXCHANGE_INFLOW = 6 # Crédito de divisa
    CURRENCY_EXCHANGE = 7 # Crédito de divisa
    DEGIRO_TRANSACTION_COMISSION = 8 # Comissão de transação
    DEGIRO_CONNECTIVITY_COST = 9 #Custo de Conectividade DEGIRO 2021 
    DEGIRO_CASH_SWEEP = 10 #Degiro Cash Sweep Transfer | #Flatex Cash Sweep Transfer
    DEPOSIT = 11 #flatex Deposit
    WITHDRAWAL = 12 #Withdrawal
    DIVIDEND = 13 # Dividendo
    DIVIDEND_TAX = 14 #Imposto sobre dividendo