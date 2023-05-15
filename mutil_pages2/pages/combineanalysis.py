import dash
from dash import html, dcc, callback, dash_table 
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State  

import os  
import io  
import base64   
import pandas as pd  

import plotly.express as px  

import numpy as np  
from sklearn.preprocessing import MinMaxScaler  


combine_st_df = pd.DataFrame() 


# 每个页面都需要用dash.register_page(name, path='/') 声明是一个页面，path='/'设置路径为根路径
dash.register_page(__name__)


# =============== 空间代谢组 数据上传页面 ===============   
control_sm_content = html.Div([
    dbc.Card(
        [
            dbc.CardHeader("展示空间代谢组内容 demo"),
            # 文件上传
            dbc.CardBody(
                [
                    html.H4("文件上传"),
                    html.P("上传空间代谢组数据，格式为csv或者xlsx"),
                    dcc.Upload(
                        id='upload-data-sm',
                        children=html.Div([
                            '拖放文件到这里或者',
                        ]),
                        style={
                            'width': '100%',
                            'height': '60px',
                            'lineHeight': '60px',
                            'borderWidth': '1px',
                            'borderStyle': 'dashed',
                            'borderRadius': '5px',
                            'textAlign': 'center',
                            'margin': '10px'
                        },
                        # Allow multiple files to be uploaded
                        # multiple=True
                    ),                   
                ]
            ),
        ] 
    ),
    html.Br(),
    # 展示上传文档内容 
    html.Div(id='sm-table-filename'), 
    dash_table.DataTable(
        id='sm-table',
        columns=[],
        data=[],
        page_size=5,
        page_action='native',
        style_table={
            'overflowX': 'scroll',
            'maxHeight': '300px', 
        },   
        style_cell={
            'font_size': '12px',
            'font_family': 'sans-serif',
            'text_align': 'left',
            'padding': '5px'
        },
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        },
    )
]) 


control_sm_plot = dbc.Card([
    html.Div(
        [
            dbc.Label('选择分析方法'),
            dcc.Dropdown(
                id='sm-plot-method',
                options=[
                    {'label': 'Scatter', 'value': 'scatter'},
                    {'label': 'Heatmap', 'value': 'heatmap'},
                    {'label': 'Volcano', 'value': 'volcano'}
                ],
                value=''
            ), 
            dbc.Label('选择上色方法'),
            dcc.Dropdown(
                id='sm-plot-color',
                options=[],
                value=''
            ),
        
        ],
        style={
            'font-size': '12px',
            'font-family': 'sans-serif',
            'text-align': 'left',
            'padding': '5px',
            'margin': '5px'  
        }
    ),
])



# ================= 空间转录组 数据上传页面 ==================   
control_st_content = html.Div([
    dbc.Card(
        [
            dbc.CardHeader("展示空间转录组内容 demo"),
            # 文件上传
            dbc.CardBody(
                [
                    html.H4("文件上传"),
                    html.P("上传空间转录组数据，格式为csv或者xlsx"),
                    dcc.Upload(
                        id='upload-data-st',
                        children=html.Div([
                            '拖放文件到这里或者',
                        ]),
                        style={
                            'width': '100%',
                            'height': '60px',
                            'lineHeight': '60px',
                            'borderWidth': '1px',
                            'borderStyle': 'dashed',
                            'borderRadius': '5px',
                            'textAlign': 'center',
                            'margin': '10px'
                        },
                        # Allow multiple files to be uploaded
                        # multiple=True
                    ),                   
                ]
            )
        ]
    ),
    html.Br(), 
    # 展示上传文档内容
    html.Div(id='st-table-filename'),
    dash_table.DataTable(
        id='st-table',
        columns=[],
        data=[],
        page_size=5,
        page_action='native',
        style_table={
            'overflowX': 'scroll',
            'maxHeight': '300px',
        },
        style_cell={
            'font_size': '12px',
            'font_family': 'sans-serif',
            'text_align': 'left',
            'padding': '5px'
        },
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        },
    )
])


control_st_plot = dbc.Card([
    html.Div(
        [
            dbc.Label('选择分析方法'),
            dcc.Dropdown(
                id='st-plot-method',
                options=[
                    {'label': 'Scatter', 'value': 'scatter'},
                    {'label': 'Heatmap', 'value': 'heatmap'},
                    {'label': 'Volcano', 'value': 'volcano'}
                ],
                value=''
            ),
            dbc.Label('选择上色方法'),
            dcc.Dropdown(
                id='st-plot-color',
                options=[],
                value=''
            ),

        ],
        style={
            'font-size': '12px',
            'font-family': 'sans-serif',
            'text-align': 'left',
            'padding': '5px',
            'margin': '5px'  
        }
    ),
])



# ================== 联合分析部分 ==================
conttrol_combine_choice = dbc.Card([
    html.Div(
        [
            '选择组学',
            dcc.Dropdown(
                id='omice_type',
                options=[
                    {'label': 'spatial metabolomics', 'value': 'sm'},
                    {'label': 'spatial transcriptomics', 'value': 'st'}
                ],
                value='st'
            ),
            
            dbc.Row([
                dbc.Col(html.P('坐标缩放low'), md=3, style={'margin': '5px'}),
                dbc.Col(dcc.Input(
                        id='scale_low',
                        type='number',
                        value=1,
                        style={
                            'borderWidth': '1px',
                            'borderStyle': 'solid',
                            'borderRadius': '5px',
                            'margin': '5px'
                        }
                        ),
                        md=4    
                )
            ]),
            
            dbc.Row([
                dbc.Col(html.P('坐标缩放high'), md=3, style={'margin': '5px'}),
                dbc.Col(dcc.Input(
                        id='scale_high',
                        type='number',
                        value=1,
                        style={
                            'borderWidth': '1px',
                            'borderStyle': 'solid',
                            'borderRadius': '5px',
                            'margin': '5px'
                        }
                        ),
                        md=4    
                )
            ]),
            
           dbc.Row([
                dbc.Col(html.P('坐标旋转'), md=3, style={'margin': '5px'}),
                dbc.Col(dcc.Input(
                        id='rotate',
                        type='number',
                        value=1,
                        style={
                            'borderWidth': '1px',
                            'borderStyle': 'solid',
                            'borderRadius': '5px',
                            'margin': '5px'
                        }
                        ),
                        md=4    
                )
            ]),
            
            dbc.Row([
                dbc.Col(html.P('坐标缩放low2'), md=3, style={'margin': '5px'}),
                dbc.Col(dcc.Input(
                        id='scale_low2',
                        type='number',
                        value=1,
                        style={
                            'borderWidth': '1px',
                            'borderStyle': 'solid',
                            'borderRadius': '5px',
                            'margin': '5px'
                        }
                        ),
                        md=4    
                )
            ]),
            
            dbc.Row([
                dbc.Col(html.P('坐标缩放high2'), md=3, style={'margin': '5px'}),
                dbc.Col(dcc.Input(
                        id='scale_high2',
                        type='number',
                        value=1,
                        style={
                            'borderWidth': '1px',
                            'borderStyle': 'solid',
                            'borderRadius': '5px',
                            'margin': '5px'
                        }
                        ),
                        md=4    
                )
            ]),
            
            dbc.Row([
                dbc.Col(html.P('坐标平移 X'), md=3, style={'margin': '5px'}),
                dbc.Col(dcc.Input(
                        id='translate_x',
                        type='number',
                        value=1,
                        style={
                            'borderWidth': '1px',
                            'borderStyle': 'solid',
                            'borderRadius': '5px',
                            'margin': '5px'
                        }
                        ),
                        md=4    
                )
            ]),
          
            dbc.Row([
                dbc.Col(html.P('坐标平移Y'), md=3, style={'margin': '5px'}),
                dbc.Col(dcc.Input(
                        id='translate_y',
                        type='number',
                        value=1,
                        style={
                            'borderWidth': '1px',
                            'borderStyle': 'solid',
                            'borderRadius': '5px',
                            'margin': '5px'
                        }
                        ),
                        md=4    
                )
            ]),
            
            html.Button('执行操作', id='paras-submit', n_clicks=0, style={'margin': '5px', 
                                                                         'borderRadius': '5px',
                                                                         'background-color': 'orange'}),
            html.Br(),
            
            html.Div(id='paras-submit-result'),
        ],
        
        # 整体样式 
        style={
            'font-size': '12px',
            'font-family': 'sans-serif',
            'text-align': 'left',
             
        } 
    )
    
])
    



# ================== 页面内容 ==================
layout = dbc.Container(
    [
        html.Br(),
        
        # =============== 1 空间代谢组数据分析 ======================  
        html.Div([
            html.H2('spatial metabolomics', style={'background-color': 'lightblue', 
                                               'border': '1px solid #C8D4E3',
                                               'padding': '10px'}),       
            dbc.Col(control_sm_content),
            html.Br(), 
            dbc.Row(
                [
                    dbc.Col(control_sm_plot, md=4),
                    dbc.Col(dcc.Graph(id='sm-plot', style={'display': 'none'}), md=8),
                ],
                # style={
                #     'border': '1px solid #C8D4E3',
                #     'padding': '10px',
                #     'background-color': '#F4F8FB'
                # }
            ),
        ],
        style={'border': '2px solid red ', 'padding': '12px', 'borderRadius': '5px',}
        ),
        html.Br(),
        html.Br(),  
        
        
        # ================== 2 空间转录组 数据 ==============================
        html.Div([
            html.H2('spatial transcriptomics', style={'background-color': 'lightblue', 
                                                'border': '1px solid #C8D4E3',
                                                'padding': '10px'}),
            dbc.Col(control_st_content),   
            html.Br(), 
            dbc.Row(
                [
                    dbc.Col(control_st_plot, md=4),
                    dbc.Col(dcc.Graph(id='st-plot', style={'display': 'none'}), md=8),  
                    
                ],
                # style={
                #     'border': '1px solid #C8D4E3',
                #     'padding': '10px',
                #     'background-color': '#F4F8FB'
                # }
            ),
          
        ],
        style={'border': '2px solid green ', 'padding': '12px', 'borderRadius': '5px',}
        ),
        html.Br(),
        html.Br(),
        
        # ========================= 3 联合分析部分  ============================ 
        html.Div([
            html.H2('Combine analysis', style={'background-color': 'lightblue', 
                                               'border': '1px solid #C8D4E3',
                                               'padding': '10px'}
                    ),
            html.Br(), 
            dbc.Row(
                [
                    dbc.Col(conttrol_combine_choice, md=4),  
                    dbc.Col(dcc.Graph(id='combine-plot', style={'display': 'none'}), md=8),
                ],
                # style={
                #     'border': '1px solid #C8D4E3',
                #     'padding': '10px',
                #     'background-color': '#F4F8FB'
                # }
            ),
            html.Br(),
            html.Br(), 
        ],
        style={'border': '2px solid blue ', 'padding': '12px', 'borderRadius': '5px',}
        ), 
        
        # ================ 4 感兴趣区域划分 ========================================
        
    ],
    
   
)


# =============================== functions ==============================================
def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',') 
    
    decoded = base64.b64decode(content_string)  
    try:
        if 'csv' in filename:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename: 
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), sep='\t')
        elif 'xlsx' in filename: 
            df = pd.read_excel(io.BytesIO(decoded))        
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    
    return df 
            


def scale_pos(df, scale_low, scale_high):
    scaler = MinMaxScaler(feature_range=(scale_low, scale_high))
    df[['x_final', 'y_final']] = scaler.fit_transform(df[['x_final', 'y_final']])  
    return df  


def rotate_pos(df, rotate):
    # 将角度转换为弧度 
    theta = np.deg2rad(rotate) 
    
    # 旋转矩阵 
    rotate_matrix = np.array([
                                [np.cos(theta), -np.sin(theta)], 
                                [np.sin(theta), np.cos(theta)]
                            ])
    
    # 将原始坐标点构成一个矩阵
    points = np.array(df[['x_final', 'y_final']].values) 
    # 旋转后的坐标点  
    new_points = np.dot(points, rotate_matrix)   
    # 将旋转后的坐标点赋值给原始数据   
    df[['x_final', 'y_final']] = new_points  
    
    return df 



def translate_pos_x(df, translate_x):
    df['x_final'] = df['x_final'] + translate_x
    return df



def translate_pos_y(df, translate_y):
    df['y_final'] = df['y_final'] + translate_y
    return df
 
 


# =============================== callbacks ==============================================
# 以下是页面的回调函数，用于实现交互功能
@callback(
    Output('sm-table', 'columns'),
    Output('sm-table', 'data'),
    Output('sm-table-filename', 'children'),
    Input('upload-data-sm', 'contents'),
    State('upload-data-sm', 'filename'),
    State('upload-data-sm', 'last_modified'),
)
def display_sm_content(contents, filename, last_modified):
    if contents is not None:
        df = parse_contents(contents, filename, last_modified) 
        columns = [{'name': col, 'id': col} for col in df.columns]
        data = df.to_dict('records') 
        return columns, data, html.H3(filename) 
    else:
        return [], [], ''
         
    
    
@callback(
    Output('sm-plot-color', 'options'),
    Input('sm-table', 'columns'),
)
def display_sm_plot_color(columns):
    return [{'label': col['name'], 'value': col['id']} for col in columns]  

    

@callback(
    Output('sm-plot', 'style'),
    Output('sm-plot', 'figure'),
    Input('sm-table', 'data'),
    Input('sm-table', 'columns'),
    Input('sm-plot-method', 'value'),
    Input('sm-plot-color', 'value'),
)
def display_sm_plot(data, columns, method, color):
    # 将反转的数据转换为正常的数据  
    df = pd.DataFrame(data, columns=[col['id'] for col in columns]) 
    if method == 'scatter':
        fig = px.scatter(df, x='x', y='y', color=color) 
        fig.update_layout(
            title='scatter plot',
            xaxis=dict(
            scaleanchor='y',
            scaleratio=1,) 
        )
    elif method == 'heatmap':
        # 绘制热图
        fig = px.imshow(df)  
    elif method == 'volcano':
        fig = ''
    else:
        return {'display': 'none'}, {
                'data': [],
                'layout': {
                    'title': 'No plot'
                }
            }
        
    return {'display': 'block'}, fig  



@callback(
    Output('st-table', 'columns'),
    Output('st-table', 'data'),
    Output('st-table-filename', 'children'),
    Input('upload-data-st', 'contents'),
    State('upload-data-st', 'filename'),
    State('upload-data-st', 'last_modified'),
)
def display_st_content(contents, filename, last_modified):
    if contents is not None:
        df = parse_contents(contents, filename, last_modified) 
        columns = [{'name': col, 'id': col} for col in df.columns]
        data = df.to_dict('records') 
        return columns, data, html.H3(filename) 
    else:
        return [], [], ''
    
    
    
@callback(
    Output('st-plot-color', 'options'),
    Input('st-table', 'columns'),
)
def display_st_plot_color(columns):
    return [{'label': col['name'], 'value': col['id']} for col in columns]  



@callback(
    Output('st-plot', 'style'),
    Output('st-plot', 'figure'),
    Input('st-table', 'data'),
    Input('st-table', 'columns'),
    Input('st-plot-method', 'value'),
    Input('st-plot-color', 'value'),
)
def display_st_plot(data, columns, method, color):
    # 将反转的数据转换为正常的数据  
    df = pd.DataFrame(data, columns=[col['id'] for col in columns]) 
    if method == 'scatter':
        fig = px.scatter(df, x='x', y='y', color=color) 
        # 解决x轴和y轴比例不一致的问题 
        fig.update_layout(
            title='scatter plot',
            xaxis=dict(
            scaleanchor='y',
            scaleratio=1,) 
        )
    elif method == 'heatmap':
        # 绘制热图
        fig = px.imshow(df)  
    elif method == 'volcano':
        fig = ''
    else:
        return {'display': 'none'}, {
            'data': [],
            'layout': {
                'title': 'No plot'
            }
        }
        
    return {'display': 'block'}, fig  



@callback(
    Output('combine-plot', 'style'),
    Output('combine-plot', 'figure'),
    Output('paras-submit-result', 'children'),
    Input('paras-submit', 'n_clicks'),
    State('st-table', 'data'),
    State('st-table', 'columns'),
    State('sm-table', 'data'),
    State('sm-table', 'columns'),
    State('omice_type', 'value'),
    State('scale_low', 'value'),
    State('scale_high', 'value'),
    State('scale_low2', 'value'),
    State('scale_high2', 'value'),
    State('rotate', 'value'),
    State('translate_x', 'value'),
    State('translate_y', 'value'),
)
def submit_paras(n_clicks, 
                 st_data,
                 st_columns,
                 sm_data, 
                 sm_columns,
                 omice_type, 
                 scale_low, 
                 scale_high,
                 scale_low2,
                 scale_high2,   
                 rotate, 
                 translate_x, 
                 translate_y):
    
    # # if not st_data or not sm_data:
    # #     return '', 'Please upload data'
    # if not st_data:
    #     return '', 'Please st upload data'
    
    # if not sm_data:
    #     return '', 'Please sm upload data'
    
    st_df = pd.DataFrame(st_data, columns=[col['id'] for col in st_columns]) 
    sm_df = pd.DataFrame(sm_data, columns=[col['id'] for col in sm_columns])  
    
    st_df['type'] = 'st'
    sm_df['type'] = 'sm' 
    
    
    st_df[['x_final', 'y_final']] = st_df[['x', 'y']]    
    sm_df[['x_final', 'y_final']] = sm_df[['x', 'y']]  
    
    merge_df = pd.concat([st_df, sm_df], axis=0).reset_index(drop=True)  
    
    handle_df = merge_df.loc[merge_df['type'] == omice_type, :]  # 选择要处理的数据
    not_handle_df = merge_df.loc[merge_df['type'] != omice_type, :]  # 不需要处理的数据 
    
    # 数据缩放
    if scale_high > scale_low:
        handle_df = scale_pos(handle_df, scale_low, scale_high) 
        
    # # 数据旋转  
    handle_df = rotate_pos(handle_df, rotate)  
    
    # 旋转后，一般需要进行二次坐标缩放 
    if scale_high2 > scale_low2:
        handle_df = scale_pos(handle_df, scale_low2, scale_high2)  
    
    # # 数据平移
    handle_df = translate_pos_x(handle_df, translate_x) 
    
    # # 数据平移 
    handle_df = translate_pos_y(handle_df, translate_y)   
    
    # # 整合后的数据  
    merge_df = pd.concat([handle_df, not_handle_df], axis=0).reset_index(drop=True)   
    
    fig = px.scatter(
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
    
    fig.update_layout(
        title='combine plot',
        xaxis=dict(
            scaleanchor='y',
            scaleratio=1,)
    )
    
    if n_clicks > 0:
        return {'display': 'block'}, fig, f'{n_clicks} 次处理'
        
        
        