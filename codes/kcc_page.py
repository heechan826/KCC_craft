#from boto import connect_ia
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
#import networkx as nx
from pyvis.network import Network
import random
import os
import utils

dict = {
    '도자기': 'Ceramic',
    '유리': 'Glass',
    '나무': 'Wood',
    '금속': 'Metal',
    '종이': 'Paper',
    '섬유': 'Textile',
    '가죽': 'Lether',
}

def show_page(type):

    # Read dataset (CSV)
    craft = pd.read_excel("/data/datas.xlsx", sheet_name=dict[type])

    craft_tmp = craft.rename(columns=lambda x: x + ': ')
    craft_tmp = craft_tmp.rename({"ID: ": "ID"}, axis=1)

    # Image path
    img_path = "C:/Users/SCI/Desktop/대표사진크롭1/"

    # Set header title
    st.title("CRAFT THINKER's TOOL")

    # Save information
    information_dict = {}
    for _, row in craft_tmp.iterrows():
        #print('[row]')
        #print(row)
        #print('len(row)')
        #print(len(row))
        for feature in range(len(row)):
            if feature == 0:
                continue
            row[feature] = str(row[feature]) + '<br> '
        #print('[row[0]]')
        #print(row[0])
        information_dict[row['ID']] = row
    '''
    for index, row in craft.iterrows():
        information_dict[row['ID']] = row
    '''

    craft = pd.read_excel("datas.xlsx", sheet_name=dict[type])

    #names = ['제작자', '형태', '용도 3']
    names = ['ID']
    options = []
    for feature in names:
        option = utils.create_options(craft, feature)
        cleanedOption = [x for x in option if str(x) != 'nan']
        selected_options = st.multiselect(feature + '를 선택해주세요 ', cleanedOption)
        options = options+selected_options

    features = ['제작자', '태토 1', '태토 2', '유약 1', '유약 2', '용도 3', '용도 4', '형태', '제작방법 1', '규격(mm)', '생산연도', '가격']
    edges_list = []
    for feature in features:
        edges = craft[['ID',feature]]
        edges_list.append(edges)
    #print(edges_list[0])

    total_edge = pd.DataFrame()
    
    for i, edges in enumerate(edges_list):
        total_edge = pd.concat([total_edge, edges.rename(columns = {features[i]: '특징'})], ignore_index = True)
    #print('[total_edge]')
    #print(total_edge)

    # Set info message on initial site load
    if len(options) == 0:
        st.text('마음에 드는 제품을 선택해주세요')

    # Create network graph when user selects >= 1 item
    else:
        #print('[options]')
        #print(options)
        df_select = total_edge.loc[total_edge['ID'].isin(options) | \
                                    total_edge['특징'].isin(options)]
        df_select = df_select.reset_index(drop=True)

        #print('df_select[특징]')
        #print(df_select['특징'])

        sources_crf = df_select['ID']
        targets_crf = df_select['특징']
        edge_data = zip(sources_crf, targets_crf)
        
        #G = nx.from_pandas_edgelist(df_select, 'ID', '특징')

        #print('df_select[특징][0]')
        #print(df_select['특징'][0])

        sources_list = []
        targets_list = []
        edge_data_list = []

        for feature in df_select['특징']:
            #tmp.append(df_select['특징'][0])
            # do not handle 
            if feature == ('기타' or 'nan'):
                continue

            tmp = []
            tmp.append(feature)
            #print('[tmp]')
            #print(tmp)
            #print('[feature]')
            #print(feature)

            df_select2 = total_edge.loc[total_edge['ID'].isin(tmp) | \
                                total_edge['특징'].isin(tmp)]
            df_select2 = df_select2.reset_index(drop=True)

            for option in options:
                in_options = df_select2['ID'].isin([option])
                df2 = df_select2[~in_options]
            try:
                df2_random = df2.sample(n=3, random_state=104)
            except ValueError:
                continue

            source = df2_random['ID']
            target = df2_random['특징']
            sources_list.append(source)
            targets_list.append(target)
            edge_data_list.append(zip(source, target))

        #print('[edge_data_list]')
        #print(edge_data_list)

        # Initiate PyVis network object
        craft_net = Network(
                        height='600px',
                        width='100%',
                        bgcolor='#222222',
                        font_color='white'
                        )

        new_imgs, id_img_dict = utils.resize_imgs(new_size = 256, dir = "대표사진크롭1", extension = 'jpg')
        st.text(id_img_dict.keys())
        st.text(id_img_dict['C00002'])
        print('id_img_dict.keys()')
        print(id_img_dict.keys())
        print('id_img_dict[C00002]')
        print(id_img_dict['C00002'])

        # 선택한 제품에 대한 feature 노드들 생성
        for index, e in enumerate(edge_data):

            src = e[0]
            dst = e[1]
            #print(id_img_dict[src])
            craft_net.add_node(src, src, size = 20, title = '', shape='circularImage', image = id_img_dict[src])

            # To get rid of '기타'
            if dst == '기타':
                continue
            # To handle NA data in each feature
            try:
                craft_net.add_node(dst, label = str(dst) + '\n[' +str(features[index]) + ']', size = 20, title= dst)
                #craft_net.add_node(n_id = (dst, dst), label="t", size = 20, title= dst)
                #craft_net.add_node(dst, dst, size = 20, title=(str(dst) + str(features[index])))
            except AssertionError:
                continue
            craft_net.add_edge(src, dst)
        for node in craft_net.nodes:
            try:
                node['title'] += str(information_dict[node['id']])
            except KeyError:
                continue
        

        # feature 노드들에 대한 추천 제품들 노드로 생성
        for i, edge_data_ in enumerate(edge_data_list):
            for e in edge_data_:

                src = e[0]
                dst = e[1]
                try:
                    craft_net.add_node(dst, dst, size = 20, title=dst)
                except AssertionError:
                    continue
                craft_net.add_node(src, src, size = 20, title=src, shape='circularImage', image = id_img_dict[src])
                craft_net.add_edge(src, dst)
            #neighbor_map = craft_net.get_adj_list()
            # add neighbor data to node hover data
            
            tmpp = 0
            for node in craft_net.nodes:
                try:
                    tmp_len = str(node['title'])
                except KeyError:
                    continue
                
                #print('[len]')
                #print(len(tmp_len))
                if len(tmp_len) < 100:
                    try:
                        node['title'] += str(information_dict[node['id']])
                        print('[len(node[title])]')
                        print(len(node['title']))
                        #print('[break]\n')
                    except KeyError:
                        continue
                else:
                    continue
            print('[break]\n')

        info_dict = {}

        #print('[information_dict[0]]')
        #print('information_dict[C00095]')
        #print(information_dict['C00095'])

        # Generate network with specific layout settings
        craft_net.repulsion(
                            node_distance=420,
                            central_gravity=0.33,
                            spring_length=110,
                            spring_strength=0.10,
                            damping=0.95
                        )
        
        if st.button('이미지와 함께 결과 보기(클릭)'):
            craft_net.show('pyvis_network_craft.html')

        # Save and read graph as HTML file (on Streamlit Sharing)
        try:
            path = os.getcwd()
            path = path + '\\tmp'
            craft_net.save_graph(f'{path}/pyvis_graph.html')
            HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

        # Save and read graph as HTML file (locally)
        except:
            path = os.getcwd()
            path = path + '\\tmp'
            print(path)
            craft_net.save_graph(f'{path}\pyvis_graph.html')
            HtmlFile = open(f'{path}\pyvis_graph.html', 'r', encoding='utf-8')

        # Load HTML file in HTML component for display on Streamlit page
        components.html(HtmlFile.read(), height=1030)
    
