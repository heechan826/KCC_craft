import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import os 
import utils 
from PIL import Image 
import random

def read_markdown(markdown_file):
        return Path(markdown_file).read_text(encoding="UTF8")

def show_page(name):

    for i in range(8):
        st.sidebar.write("")
    intro_markdown = read_markdown("/docs/introduction.md")
    st.markdown(intro_markdown)

    if st.button('이미지 다시 생성(클릭)'):
        a = 1

    new_imgs, id_img_dict = utils.resize_imgs(new_size = 256, dir = "대표사진크롭1", extension = 'jpg')
    new_imgs = new_imgs[:1774]

    #opening the image
    images = []
    col1, col2, col3 = st.columns(3) 

    for i in range(3):
        #print(len(new_imgs))
        indexs = []
        select_imgs = []
        imgs = []
        imgs_names = []
        for i in range(3):
            index = random.randint(0, len(new_imgs))
            select_img = new_imgs[index-1]
            print(select_img)
            img = Image.open(select_img)
            img_name = select_img.split('/')[-1]
            img_name = img_name.split('_')[0]
            print('img_name')
            print(img_name)
            imgs.append(img)
            imgs_names.append(img_name)

        with col1:
            st.image(imgs[0], width = 250, caption=imgs_names[0])

        with col2:
            st.image(imgs[1], width = 250, caption=imgs_names[1])

        with col3:
            st.image(imgs[2], width = 250, caption=imgs_names[2])

    '''
    path = os.getcwd()
    path = path + '\\..\\tmp'
    HtmlFile = open(f'{path}\pyvis_graph_2.html', 'r', encoding='utf-8')

    # Load HTML file in HTML component for display on Streamlit page
    components.html(HtmlFile.read(), height=630)
    '''
