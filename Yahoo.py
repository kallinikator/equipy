import requests
from urllib.parse import urlencode

"""
This are the needed urls for the API of Yahoo.
"""
PUBLIC_API_URL  = 'http://query.yahooapis.com/v1/public/yql'
DATATABLES_URL  = 'store://datatables.org/alltableswithkeys'


def prepare_query(symbol, table='quotes', key='symbol'):
    """ A Simple YQL query builder """
    query = 'select * from yahoo.finance.{table} where {key} = "{symbol}"'.format(symbol=symbol, table=table, key=key)
    return query


def query(symbol: str):
    """ Queries the Yahoo finance API. """
    yql = prepare_query(symbol)
    api_request = requests.get(PUBLIC_API_URL + '?' + urlencode({ 'q': yql, 'format': 'json', 'env': DATATABLES_URL }))

    return api_request.json()


if __name__ == "__main__":
    yql = prepare_query("GOOG")
    connection = requests.get(PUBLIC_API_URL + '?' + urlencode({ 'q': yql, 'format': 'json', 'env': DATATABLES_URL }))