import pandas as pd
from googleTrends import GoogleTrendsAPI


API = GoogleTrendsAPI


# geoName lat lon geoCode timeframe words ......
def getDataByRegionAndOvertime(kw_list: list, timeframe_list: list):
    result = []
    if not kw_list or not timeframe_list:
        return None
    for timeframe in timeframe_list:
        heatValue = []
        for kw in kw_list:
            data = API.getDataByRegion(kw, timeframe)
            if data is not None:
                heatValue.append(data)
        var: pd.DataFrame = pd.concat(heatValue, axis=1).T.drop_duplicates().T
        var.insert(1, 'timeframe', timeframe)
        result.append(var)
    df = pd.concat(result)
    return API.addGeo(df)


# time words ......
def getDataOvertimeMultiWord(kw_list: list, timeframeOrList: str | list):
    result = []
    for timeframe in timeframeOrList:
        heatValue = []
        for kw in kw_list:
            heatValue.append(API.getDataOvertime(kw, timeframe))
        var = pd.concat(heatValue, axis=1).T.drop_duplicates().T
        var.insert(1, 'timeframe', timeframe)
        result.append(var)
    df = pd.concat(result)
    return df
