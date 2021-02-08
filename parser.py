import csv
import json
import os
import urllib.request
import urllib.parse

FILENAME = 'dataset/account.csv'

openfigi_apikey = os.environ['OPENFIGI_API_KEY'] 

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


def map_jobs(jobs):
    '''
    Send an collection of mapping jobs to the API in order to obtain the
    associated FIGI(s).
    Parameters
    ----------
    jobs : list(dict)
        A list of dicts that conform to the OpenFIGI API request structure. See
        https://www.openfigi.com/api#request-format for more information. Note
        rate-limiting requirements when considering length of `jobs`.
    Returns
    -------
    list(dict)
        One dict per item in `jobs` list that conform to the OpenFIGI API
        response structure.  See https://www.openfigi.com/api#response-fomats
        for more information.
    '''
    handler = urllib.request.HTTPHandler()
    opener = urllib.request.build_opener(handler)
    openfigi_url = 'https://api.openfigi.com/v2/mapping'
    request = urllib.request.Request(openfigi_url, data=bytes(json.dumps(jobs), encoding='utf-8'))
    request.add_header('Content-Type','application/json')
    if openfigi_apikey:
        request.add_header('X-OPENFIGI-APIKEY', openfigi_apikey)
    request.get_method = lambda: 'POST'
    connection = opener.open(request)
    if connection.code != 200:
        raise Exception('Bad response code {}'.format(str(response.status_code)))
    return json.loads(connection.read().decode('utf-8'))


def main():
    data = {}
    jobs = []
    transactions = []
    with open(FILENAME) as csvfile:
        for idx,row in enumerate(csv.DictReader(csvfile)):
            
            #Parses the ISIN and gets the ticker of the company 
            if row['ISIN'] != '':
                jobs.append({'idType': 'ID_ISIN', 'idValue': row['ISIN'], 'exchCode': 'US'})

            #openfigi supports a maximum of 100 jobs per request
            if len(jobs) == 100:
                ticker_info = { e['ticker']:e for e in [_['data'][0] for _ in map_jobs(jobs) if 'error' not in _]}
                jobs.clear()
                data.update(ticker_info)
            
            #if row['Descrição']


    with open('output.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)



if __name__=='__main__':
    main()