from django.core.management import BaseCommand

from currency.helper import RateManager, CurrencyManager


class Command(BaseCommand):
    help = 'get data from curl https://api-pub.bitfinex.com/v2/candles/trade:1m:tBTCUSD/last'

    def handle(self, *args, **kwargs):
        cm = CurrencyManager()
        cm.get_by_mask()

        rm = RateManager()
        rm.update_rate(time="1M")
        rm.clear_history(days=20)
