import plotly.graph_objects as go
import plotly.express as px
import requests
import streamlit as st


# 动态请求bing api接口
@st.cache_data
def getmapsource():
    bing_map_token = 'AlokyiLvd54vljDRnjUfkF_STJ2nGNZ9N1j_FAFtAMERXrTc57hJdKRyq6yc2EDk'
    req = requests.get('https://dev.virtualearth.net/REST/V1/Imagery/Metadata/CanvasLight?output=json&include'
                       '=ImageryProviders&uriScheme=https&key={BingMapsKey}'.format(BingMapsKey=bing_map_token))
    url_json = req.json()['resourceSets'][0]['resources'][0]
    sources = [url_json['imageUrl'].replace('{subdomain}', sub) for sub in
               url_json['imageUrlSubdomains']]
    return sources


def create_line_chart(df_time, keyword):
    fig = px.line(df_time, x=df_time.index, y=keyword, labels={keyword: 'Popularity'})
    fig.update_layout(title=f'Time-wise "{keyword}" Popularity')
    return fig


def create_bar_chart(df_country, keyword):
    fig = px.bar(df_country, y='geoCode', x=keyword, labels={keyword: 'Popularity'})
    fig.update_layout(title=f'Country-wise "{keyword}" Popularity')
    return fig


def create_density_mapbox_chart(df_country, keyword):
    # 颜色表
    COLOR_MAP = [
        [0.0, "#00FF00"],
        [0.3, '#BDDF31'],
        [0.4, '#FFFF00'],
        [0.6, '#FF6600'],
        [1, "red"]
    ]
    fig = px.density_mapbox(df_country, lat='lat', lon='lon', z=keyword, labels={keyword: 'Popularity'}, zoom=3)
    fig.update_layout(title=f'Country-wise "{keyword}" Popularity')
    fig.update_layout(mapbox=dict(style="white-bg",
                                  layers=[
                                      dict(
                                          below="traces",
                                          sourcetype="raster",
                                          # 地图提供商
                                          sourceattribution="Bing Map",
                                          # 地图块请求api
                                          source=getmapsource()
                                      )
                                  ]
                                  ), )
    return fig
