import dash  
from dash import html, dcc, callback, Input, Output 

dash.register_page(__name__) 

layout = html.Div([
    html.H1('散点图跳转页面') 
])