import json
import urllib.request
import urllib.parse
import os

class OpenFIGI:

    @staticmethod
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
        if os.environ['OPENFIGI_API_KEY'] :
            request.add_header('X-OPENFIGI-APIKEY', os.environ['OPENFIGI_API_KEY'] )
        request.get_method = lambda: 'POST'
        connection = opener.open(request)
        if connection.code != 200:
            raise Exception('Bad response code {}'.format(str(response.status_code)))
        return json.loads(connection.read().decode('utf-8'))