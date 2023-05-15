import dash  
from dash import html, dcc, callback, Input, Output 

dash.register_page(__name__, '/plot_demo')


layout = html.Div([
    html.H1('Plot Demo'),
    html.Div([
        'select a city: ',  
        dcc.RadioItems(['Beijing', 'Shanghai', 'Guangzhou'], 'Beijing', id='city')
    ]),
    html.Br(),
    html.Div(id='output-plot'),
    html.Hr(), 
    dcc.Link('散点图', href='/scatter', style={'margin': '10px'}), 
    dcc.Link('气泡图', href='', style={'margin': '10px'}),
    dcc.Link('条形图', href='', style={'margin': '10px'})  
])

# # ==================== Callback ====================
@callback(
    Output('output-plot', 'children'),
    Input('city', 'value')
)
def update_plot(city):
    return f'You have selected {city}.'


