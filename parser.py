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
    #...


if __name__=='__main__':
    main()