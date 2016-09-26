import requests
from urllib.parse import urlencode

"""
This are the needed urls for the API of Yahoo.
"""
PUBLIC_API_URL  = 'http://query.yahooapis.com/v1/public/yql'
DATATABLES_URL  = 'store://datatables.org/alltableswithkeys'

def prepare_query(symbol, table='quotes', key='symbol'):
	"""
	Simple YQL query builder
	"""
	query = 'select * from yahoo.finance.{table} where {key} = "{symbol}"'.format(
		symbol=symbol, table=table, key=key)

	return query


def query(symbol: str):
    """
    Queries the Yahoo finance API. 
    """
    yql = prepare_query(symbol)
    api_request = requests.get(PUBLIC_API_URL + '?' + urlencode({ 'q': yql, 'format': 'json', 'env': DATATABLES_URL }))

    return api_request.json()


#class Share(object):

#    def __init__(self, symbol):
#        super(Share, self).__init__(symbol)
#        self._table = 'quotes'
#        self._key = 'symbol'
#        self.refresh()

#    def fetch(self):
#        data = super(Share, self)._fetch()
#        if data['LastTradeDate'] and data['LastTradeTime']:
#            data[u'LastTradeDateTimeUTC'] = edt_to_utc('{0} {1}'.format(data['LastTradeDate'], data['LastTradeTime']))
#        return data

#    def get_historical(self, start_date, end_date):
#        """
#        Get Yahoo Finance Stock historical prices

#        :param start_date: string date in format '2009-09-11'
#        :param end_date: string date in format '2009-09-11'
#        :return: list
#        """
#        hist = []
#        for s, e in get_date_range(start_date, end_date):
#            try:
#                query = self._prepare_query(table='historicaldata', startDate=s, endDate=e)
#                result = self._request(query)
#                if isinstance(result, dict):
#                    result = [result]
#                hist.extend(result)
#            except AttributeError:
#                pass
#        return hist

#    def get_info(self):
#        """
#        Get Yahoo Finance Stock Summary Information

#        :return: dict
#        """
#        query = self._prepare_query(table='stocks')
#        return self._request(query)

if __name__ == "__main__":
    yql = prepare_query("GOOG")
    connection = requests.get(PUBLIC_API_URL + '?' + urlencode({ 'q': yql, 'format': 'json', 'env': DATATABLES_URL }))