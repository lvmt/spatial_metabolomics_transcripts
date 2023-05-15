# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go 



# Incorporate data
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

# Initialize the app - incorporate css
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets) 


df1 = pd.read_csv('../sm.xls', sep='\t')
df2 = pd.read_csv('../st.xls', sep='\t')

# app layout  
app.layout = html.Div([
    html.Div(className='row', 
             children=[
                html.Div(className='six columns', 
                         children=[
                                dcc.Graph(figure={}, id='figure_plot')
                                ]
                         
                        ),
                
                
                html.Div(className='six columns', 
                         children=[ html.P('绘制选择的图形'),
                                    dcc.Dropdown(['figure1', 'figure2', 'all'], id='plot_who'), 
                                    html.Br(),
                            
                                    html.P('旋转角度'), 
                                    dcc.Input(type='text', placeholder='请输入旋转角度', id='rotate_angle', value='0'),
                                    html.Br(),
                                    
                                    html.P('水平移动方向'),
                                    dcc.Input(placeholder='请输入水平移动方向', type='text', id='move_direction_x'),
                                    html.Br(),
                                    
                                    html.P('垂直移动距离'),
                                    dcc.Input(placeholder='请输入垂直移动距离', type='text', id='move_distance_y'),
                                    html.Br(),
                                    
                                    html.P('缩放比例'),
                                    dcc.Input(placeholder='请输入缩放比例', type='text', id='scale_ratio'), 
                                    
                                    
                                    ]
                         )
             ]       
            )
    ]) 


callback(
    Output(component_id='figure_plot', component_property='figure'),
    Input(component_id='rotate_angle', component_property='value')
)
def plot(angle):
    print(angle) 
    fig = px.scatter(df1, x='x', y='y') 
    # fig = go.Figure(data=[go.Scatter(x=df1['x'], y=df1['y'], mode='markers', name='file1'),
    #                       go.Scatter(x=df2['x'], y=df2['y'], mode='markers', name='file2')]) 
    
    return fig
    


if __name__ == '__main__':
    app.run_server(debug=True) 