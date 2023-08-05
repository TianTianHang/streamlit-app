import json

import pandas as pd
import streamlit as st
from requests import ConnectTimeout
from streamlit_extras.no_default_selectbox import selectbox

from service import TrendsService
from service.WordsService import get_all_words
from utils.plot_utils import create_density_mapbox_chart, create_bar_chart, create_line_chart
from utils.timeframe_generate import generate_time_range_options

st.set_page_config(
    page_title="google trends",
    page_icon="🎢",
    layout='wide'
)


@st.cache_data
def load_gprop_options():
    gprop_df = pd.read_json('resource/static/GoogleTrendsGprop.json', orient='records')
    return gprop_df.to_dict(orient='records')


@st.cache_data
def load_categorys_options():
    with open('resource/static/GoogleTrendsCategorys.json', 'r') as f:
        categorys_json = json.load(f)
    return categorys_json


@st.cache_data
def get_interest_by_region(keyword, timeframe, geo, cat, gprop):
    if st.session_state.trends:
        return st.session_state.trends.get_interest_by_region(keyword=keyword, timeframe=timeframe, geo=geo, cat=cat,
                                                              gprop=gprop)
    else:
        return None


@st.cache_data
def get_interest_over_time(keyword, timeframe, geo, cat, gprop):
    if st.session_state.trends:
        return st.session_state.trends.get_interest_over_time(keyword=keyword, timeframe=timeframe, geo=geo, cat=cat,
                                                              gprop=gprop)
    else:
        return None


@st.cache_data
def get_related_queries(keyword, timeframe, geo, cat, gprop):
    if st.session_state.trends:
        return st.session_state.trends.get_related_queries(keyword=keyword, timeframe=timeframe, geo=geo, cat=cat,
                                                           gprop=gprop)
    else:
        return None


@st.cache_data
def get_related_topics(keyword, timeframe, geo, cat, gprop):
    if st.session_state.trends:
        return st.session_state.trends.get_related_topics(keyword=keyword, timeframe=timeframe, geo=geo, cat=cat,
                                                          gprop=gprop)
    else:
        return None


def selector_change(level):
    options = st.session_state[f'category-{level - 1}']
    st.session_state.category = {'name': options['name'], 'id': options['id']}
    if 'children' in options:
        st.session_state.category_level = level
    else:
        st.session_state.category_level = level - 1


st.write("Google Trends")
# 在这里可以添加你的应用主页面代码
all_words = get_all_words(st.session_state.db_session)
gprop_options = load_gprop_options()
categorys_options = load_categorys_options()

keyword = st.text_input(label='kw', label_visibility='hidden', placeholder='Add a search term')
st.write(keyword)
with st.container():
    cols = st.columns(4)

    with cols[0]:
        country_options = [{'geoName': 'Worldwide',
                            'geoCode': ''}]
        country_options.extend(st.session_state.df_loc.to_dict(orient='records'))
        country = st.selectbox(label='country', label_visibility='hidden',
                               options=country_options,
                               format_func=lambda e: e['geoName'])
        st.write(country)
    with cols[1]:
        time_range = st.selectbox(label='time_range', label_visibility='hidden',
                                  options=generate_time_range_options(),
                                  format_func=lambda e: e['label'])
        st.write(time_range)
    with cols[2]:
        selectbox(label='category', label_visibility='hidden', options=categorys_options['children'],
                  format_func=lambda e: e['name'], on_change=selector_change, key='category-1',
                  kwargs=dict(level=2), no_selection_label=categorys_options)
        if "category_level" in st.session_state:
            for level in range(2, st.session_state.category_level + 1):
                options = st.session_state[f'category-{level - 1}']
                if 'children' in options:
                    selectbox(label=f'category-{level}', label_visibility='hidden',
                              options=options['children'], format_func=lambda e: e['name'],
                              on_change=selector_change, key=f'category-{level}',
                              no_selection_label={"name": f'select level-{level} category', "id": -1},
                              kwargs=dict(level=level + 1))
        st.write(st.session_state.get('category', {"name": "All categories", "id": 0}))
        cat = st.session_state.get('category', {}).get('id', 0)

    with cols[3]:
        gprop = st.selectbox(label='gprop', label_visibility='hidden', options=gprop_options,
                             format_func=lambda e: e['label'])
        st.write(gprop)


def retry_trends():
    try:
        st.session_state.trends = TrendsService()
        st.session_state.trends_message = 'success'
    except ConnectTimeout as e:
        st.session_state.trends_message = e


st.sidebar.button('重新连接Google Trends', on_click=retry_trends)
trends_message = st.session_state.get('trends_message', '')
if trends_message is Exception:
    st.sidebar.error(trends_message)
else:
    st.sidebar.write(trends_message)

with st.container():
    cols = st.columns(2)
    df_country = get_interest_by_region(keyword=keyword, timeframe=time_range['value'], cat=cat,
                                        gprop=gprop['value'], geo=country['geoCode'])
    df_country_with_location = st.session_state.df_loc.merge(df_country, on='geoCode')
    st.dataframe(df_country_with_location)
    df_time = get_interest_over_time(keyword=keyword, timeframe=time_range['value'], cat=cat,
                                     gprop=gprop['value'], geo=country['geoCode'])
    with cols[0]:
        st.plotly_chart(create_line_chart(df_country, keyword))
    with cols[1]:
        st.plotly_chart(create_bar_chart(df_country, keyword))
    st.plotly_chart(create_density_mapbox_chart(df_country_with_location, keyword))
