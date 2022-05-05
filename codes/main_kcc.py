import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import networkx as nx
from pyvis.network import Network
import random
import os
import utils
import kcc_page as C
import intro_kcc as intro

#Sidebar settings

#logo, name = st.sidebar.columns(2)
#with logo:
#    image = 'hedoes_logo.png'
#    st.image(image, use_column_width=True)

st.sidebar.write(" ")

pages = {
        "사용 방법": intro,
        "도자기": C,
        "유리": C,
        "나무": C,
        "금속": C,
        "종이": C,
        "섬유": C,
        "가죽": C,
    }

st.sidebar.title("제품의 재질 선택하기")

# Radio buttons to select desired option
page = st.sidebar.radio("", tuple(pages.keys()))

#print(page)
pages[page].show_page(page)