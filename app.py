import pandas as pd
import streamlit as st

from model import session_maker
from service import TrendsService


def initialize_app():
    try:
        st.session_state.df_loc = pd.read_csv('resource/data/geo_country_with_location.csv', sep=',')
        st.session_state.db_session = session_maker()
        st.session_state.trends = TrendsService()
        initialized = True
    except Exception as e:
        st.error(f"类初始化出错: {e}")
        initialized = False

    return initialized


def main():
    st.title("app")

    if 'initialized' not in st.session_state:
        st.session_state.initialized = False

        # 初始化类
    if not st.session_state.initialized:
        initialized = initialize_app()
        st.session_state.initialized = initialized

    # 如果初始化成功，则显示应用的主页面
    if st.session_state.initialized:
        st.write("应用的主页面")
    else:
        st.write("初始化失败，请重试")
        st.experimental_rerun()


if __name__ == '__main__':
    st.set_page_config(
        page_title="app",
        page_icon="👋",
    )
    main()
