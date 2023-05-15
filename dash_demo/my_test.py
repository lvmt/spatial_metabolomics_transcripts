from dash import Dash, dcc, html, Input, Output
import plotly.express as px  
from plotly import data 
import pandas as pd 
import dash_daq_demo as daq   
import dash_bootstrap_components as dbc  

import io
from base64 import b64encode
import numpy as np  
from sklearn.preprocessing import MinMaxScaler  

buffer = io.StringIO()
html_bytes = buffer.getvalue().encode()
encoded = b64encode(html_bytes).decode()


df = pd.read_csv('test.xls', sep='\t') 
# df = data.iris()


app = Dash(__name__, external_stylesheets=[dbc.themes.SPACELAB]) 
which_omic = [{'label': '空转', 'value': 'st'}, {'label': '空代', 'value': 'sm'}]
app.layout = html.Div(
    [
        html.H2('空转空代点图匹配示例', style={"textAlign": "center"}, className="bg-primary text-white p-2 m-1"),
        '1 选择进行坐标旋转的组学数据',
        dcc.Checklist(
            options=which_omic,
            inline=True,
            value=['st', 'sm'],
            id='whichomic'
        ),
        
        '2 坐标缩放范围:(low, high)',
        dcc.Input(id='scale_low', type='number', value=0),
        dcc.Input(id='scale_high', type='number', value=-1),
        html.Br(),
        
        '3 坐标旋转角度:',
        dcc.Input(id='rotate_angle', type='number', value=0),
        html.Br(),
        
        '4 坐标缩放:(low, high)',
        dcc.Input(id='scale_low2', type='number', value=0),
        dcc.Input(id='scale_high2', type='number', value=-1),
        html.Br(),
        
        '5 坐标左右平移:',
        dcc.Input(id='translate_x', type='number', value=0), 
        html.Br(),
        
        '6 坐标上下移动:',
        dcc.Input(id='translate_y', type='number', value=0),
        html.Br(), 
        
        dbc.Card(dcc.Graph(id='graph')), 
        dbc.Card(dcc.Graph(id='graph2')),
        dbc.Card(dcc.Graph(id='graph3')),
        dbc.Card(dcc.Graph(id='graph4')),
    

    ]
    
)


# 根据条件，更新坐标
def scale_pos(df, scale_low, scale_high):
    scaler = MinMaxScaler(feature_range=(scale_low, scale_high))
    df[['x_final', 'y_final']] = scaler.fit_transform(df[['x_final', 'y_final']])
    return df    


def rotate_pos(df, rotate_angle):
    # 将角度转换为弧度 
    theta = np.deg2rad(rotate_angle) 
    
    # 旋转矩阵  
    rotation_matrix = np.array([[np.cos(theta), -np.sin(theta)], 
                                [np.sin(theta),  np.cos(theta)]])
    
    # 将原始坐标点构成一个矩阵
    points = np.array(df[['x_final', 'y_final']].values) 
    # 计算新的坐标点  
    new_points = np.dot(points, rotation_matrix)  
    # 更新坐标  
    df[['x_final', 'y_final']] = new_points 
    
    return df 


def translate_pos_x(df, translate_x):
    # 左右平移
    df['x_final'] = df['x_final'] + translate_x 
    return df 


def translate_pos_y(df, translate_y):
    df['y_final'] = df['y_final'] + translate_y  
    return df 



@app.callback(
    Output('graph', 'figure'),
    Output('graph2', 'figure'),
    Output('graph3', 'figure'),
    Output('graph4', 'figure'),
    Input('whichomic', 'value'),
    Input('scale_low', 'value'),
    Input('scale_high', 'value'),
    Input('rotate_angle', 'value'),
    Input('scale_low2', 'value'),
    Input('scale_high2', 'value'),
    Input('translate_x', 'value'),
    Input('translate_y', 'value'),
)
def update_fig(omic,scale_low, scale_high, rotate_angle, scale_low2, scale_high2, translate_x, translate_y):
    
    df[['x_final', 'y_final']] = df[['x', 'y']]
    
    st_df = df.loc[df['type'] == 'st']  # 选择要处理的数据
    sm_df = df.loc[df['type'] == 'sm']  # 选择要处理的数据 
    
    handle_df = df.loc[df['type'].isin(omic)]  # 选择要处理的数据
    not_handle_df = df.loc[~df['type'].isin(omic)]  # 不需要处理的数据 
    
    # 第一次缩放
    if scale_high <= scale_low:
        print('no scale')
    else:
        handle_df = scale_pos(handle_df, scale_low, scale_high)  # 缩放处理 
        
    # 旋转操作
    handle_df = rotate_pos(handle_df, rotate_angle)  
    
    # 旋转之后再次缩放  
    if scale_high2 <= scale_low2:
        print('no scale')
    else:
        handle_df = scale_pos(handle_df, scale_low2, scale_high2) # 缩放处理
    
    # 平移操作
    handle_df = translate_pos_x(handle_df, translate_x) 
    
    # 平移操作
    handle_df = translate_pos_y(handle_df, translate_y)  
    
    # 整合显示缩放后的数据 
    merge_df = pd.concat([handle_df, not_handle_df], axis=0)
    
    # 画图 
    fig = px.scatter(
        st_df,
        x='x_final',
        y='y_final',
        color='type',
        title='空转数据',
        labels={'x_final': 'X', 'y_final': 'Y'},
        width=800,
        height=600,
    )
    
    fig.update_layout(legend_title_text='Species') 
    

    # 画图
    fig2 = px.scatter(
        sm_df,
        x='x_final',
        y='y_final',
        color='type',
        title='空代数据',
        labels={'x_final': 'X', 'y_final': 'Y'},
        width=800,
        height=600,
    )
    
    fig3 = px.scatter(
        handle_df,
        x='x_final',
        y='y_final',
        color='type',
        title='处理结果',
        labels={'x_final': 'X', 'y_final': 'Y'},
        width=800,
        height=600,
    )
    
    fig4 = px.scatter(
        merge_df,
        x='x_final',
        y='y_final',
        color='type',
        title='空转空代匹配结果',
        labels={'x_final': 'X', 'y_final': 'Y'},
        width=800,
        height=600,
        opacity=0.5,
    )
    
    return fig, fig2, fig3, fig4



if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_props_check=True)
    
    