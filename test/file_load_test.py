import json

import pandas as pd

from service import TrendsService

df = pd.read_csv('resource/data/geo_country_with_location.csv')
d = df.to_dict(orient='records')
print(d)
