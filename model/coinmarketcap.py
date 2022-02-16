from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import time

def checkAPI_coin_id( symbol = None ):
    
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map?symbol='+ symbol
    
    #print(url)

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'ea780b61-554b-43e6-81d4-5af80a9a974d'
    }

    session = Session()
    session.headers.update(headers)

    try:
        session.headers.update(headers)
        response = session.get(url)
        data = response.json()
        aux = data["data"]
        #print(aux)
        return aux
    except :
        session.close()
        time.sleep(10)
        session = Session()
        session.headers.update(headers)
        response = session.get(url)
        data = response.json()
        try :
            aux = data["data"]
            #print(aux)
            return aux
        except :
            return None
    
def checkAPI_byid_latest(idcoin):

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?id='+idcoin
    
    #print(url)

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'ea780b61-554b-43e6-81d4-5af80a9a974d'
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url)
        data = response.json()
        aux = data["data"][idcoin]
        #print(aux)
        return aux
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return None


def checkAPI():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start':'1',
        'limit':'6',
        'convert':'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'ea780b61-554b-43e6-81d4-5af80a9a974d'
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        return data
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return None

def checkAPI_info(list_id_symbols):
    newones = ""
    for id in list_id_symbols:
        newones = newones+ str(id) +","

    #print(newones)
    string_result = newones[0:len(newones)-1]
    #print(string_result)

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/info?id='+string_result

   # print(url)

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'ea780b61-554b-43e6-81d4-5af80a9a974d'
    }

    session = Session()
    session.headers.update(headers)
    
    try:
        response = session.get(url)
        data = response.json()
        # aux = data["data"]
        # list_logo = []
        # for eachid in list_id_symbols:
        #     aux_2 = aux[str(eachid)]
        #     final_aux = aux_2["logo"]
        #     list_logo.append(final_aux)
        
        # return list_logo 
        return data 
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return None

def checkAPI_byid(id):

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/info?id='+id

    #print(url)

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'ea780b61-554b-43e6-81d4-5af80a9a974d'
    }

    session = Session()
    session.headers.update(headers)
    
    try:
        response = session.get(url)
        data = json.loads(response.text)
        
        return data 
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return None

def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"