from pytrends.request import TrendReq
from requests import ConnectTimeout


class TrendsService:
    def __init__(self):
        try:
            self.pytrends = TrendReq(hl='en-US', tz=360, timeout=(10, 25), retries=2,
                                     backoff_factor=0.1, requests_args={'headers': {}})
        except ConnectTimeout as e:
            raise e

    def get_interest_over_time(self, keyword, cat=0, timeframe='today 5-y', geo='', gprop='',):
        self.pytrends.build_payload([keyword], cat=cat, timeframe=timeframe, geo=geo, gprop=gprop)
        data = self.pytrends.interest_over_time()
        return data

    def get_interest_by_region(self, keyword, cat=0, timeframe='today 5-y', geo='', gprop='', resolution='COUNTRY'):
        self.pytrends.build_payload([keyword], cat=cat, timeframe=timeframe, geo=geo, gprop=gprop)
        data = self.pytrends.interest_by_region(resolution=resolution, inc_low_vol=True, inc_geo_code=True)
        return data

    def get_related_topics(self, keyword, cat=0, timeframe='today 5-y', geo='', gprop='',):
        self.pytrends.build_payload([keyword], cat=cat, timeframe=timeframe, geo=geo, gprop=gprop)
        data = self.pytrends.related_topics()

        return data

    def get_related_queries(self, keyword, cat=0, timeframe='today 5-y', geo='', gprop='',):
        self.pytrends.build_payload([keyword], cat=cat, timeframe=timeframe, geo=geo, gprop=gprop)
        data = self.pytrends.related_queries()
        return data
