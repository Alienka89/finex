import datetime
from re import fullmatch

import requests
from django.db.utils import IntegrityError

from currency.models import Currency, Rate


class CurrencyManager:
    url = "https://api-pub.bitfinex.com/v2/tickers?symbols=ALL"

    def get_by_mask(self, mask: str = 't[A-Z]{3}USD'):
        """
        update currencies by mask
        :param self:
        :param mask: regex string = t[A-Z]{3}USD
        :return: None
        """
        r = requests.get(self.url)
        for i in r.json():
            name = i[0]
            if fullmatch(mask, name):
                try:
                    Currency.objects.create(name=name)
                except IntegrityError:
                    pass


class RateManager:
    time_frame = ['1m', '5m', '15m', '30m', '1h', '3h', '6h', '12h', '1D', '7D', '14D', '1M']
    section = {
        "last": "last",
        "hist": "hist"
    }
    period = ["p30"]
    sort = [-1, 0, 1]
    limit = [0, 5000]

    def clear_history(self, days: int):
        """
        :param days: save data for last days
        :return: None
        """
        interval = datetime.datetime.now() - datetime.timedelta(days=days)
        Rate.objects.exclude(date__gt=interval).delete()

    def update_rate(self, time: str, max_count: int = None):
        """
        update history of rates
        :param time: value from https://docs.bitfinex.com/v2/reference#rest-public-candles TimeFrame
        :return: None
        """
        self.get_rate(type="hist", time=time, max_count=max_count)

    def _bitfinex_query(self, time: str, currency_name: str, type: str):
        try:
            url = 'https://api-pub.bitfinex.com/v2/candles/trade:{time}:{currency}/{section}'.format(
                time=time,
                currency=currency_name,
                section=self.section[type]
            )
            r = requests.get(url)
            return r.json()
        except:
            return {'error': 'Bad request'}

    def get_rate(self, time: str = '1m', type: str = "hist", currency_list=None, max_count: int = None):
        time = time if time in self.time_frame else self.time_frame[0]
        currency_list = currency_list if currency_list else Currency.objects.all()
        if max_count:
            currency_list = currency_list[:max_count]
        for currency in currency_list:
            query = self._bitfinex_query(time, currency.name, type)
            if 'error' in query:
                # TODO: write to log
                continue
            for i in query:
                mts, rate, volume = i[0], i[2], i[5]
                date = datetime.date.fromtimestamp(mts / 1000.0)
                try:
                    Rate.objects.create(mts=mts, currency=currency, date=date, rate=rate, volume=volume)
                except IntegrityError:
                    pass

    def get_last(self, pk):
        currency = Currency.objects.get(id=pk)
        query = self._bitfinex_query('1m', currency.name, 'last')
        if 'error' in query:
            return query
        return {"rate": query[2], "volume": query[5]}
