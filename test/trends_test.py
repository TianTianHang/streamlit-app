from service import TrendsService

trends = TrendsService()
df = trends.get_interest_over_time(keywords='new', timeframe="2023-07-23T21 2023-07-23T22", cat=0, gprop='')
print(df)