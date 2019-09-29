from django.test import TestCase, Client

from currency.helper import CurrencyManager, RateManager
from currency.models import Currency, Rate


class RateTestCase(TestCase):
    def setUp(self):
        cm = CurrencyManager()
        cm.get_by_mask()
        rm = RateManager()
        rm.update_rate(time="1M", max_count=5)
        Currency.objects.create(name="bad_test")

    def test_bitfinex_status(self):
        c = Client()
        response = c.get('https://api-pub.bitfinex.com/v2/platform/status')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, "[1]")

    def test_currency_uploaded(self):
        currency = Currency.objects.all()
        self.assertEqual(len(currency) > 1, True)

    def test_rate_uploaded(self):
        currency = Currency.objects.all().first()
        rate = Rate.objects.filter(name=currency.name)
        self.assertEqual(bool(rate), True)

    def test_nonexistent_currency(self):
        currency = Currency.objects.filter(name="bad_test").first()
        rate = Rate.objects.filter(name=currency.name)
        self.assertEqual(bool(rate), False)

    def test_url_doc(self):
        c = Client()
        response = c.get('/doc/')
        self.assertEqual(response.status_code, 401)
