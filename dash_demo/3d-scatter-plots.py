from dash import Dash, dcc, html, Input, Output 
import plotly.express as px  


df = px.data.iris() 

app = Dash(__name__) 

app.layout = html.Div(
    [
        html.H4('Iris Data Set'),
        dcc.Graph(id='graph'),
        html.P('Petal Width'),
        dcc.RangeSlider(
            id='range-slider',
            min=0,
            max=2.5,
            step=0.1,
            marks={0: '0', 2.5: '2.5'},
            value=[0.5, 2],
        ),
        dcc.RangeSlider(
            id='sepal_width_range',
            min=0,
            max=5,
            step=0.4,
            marks={0: '0', 5: '5'},
            value=[0, 5]
        ),
        dcc.RangeSlider(
            id='sepal_length_range',
            min=0,
            max=8,
            step=0.4,
            marks={0: '0', 8: '8'},
            value=[0, 8]
        )
            
    ]
)



@app.callback(
    Output('graph', 'figure'),
    [Input('range-slider', 'value'), Input('sepal_width_range', 'value'), Input('sepal_length_range', 'value')]
)
def update_chart(slider_range, sepal_width_range, sepal_length_range):
    low, high = slider_range
    p_l_l, p_l_h = sepal_length_range 
    p_w_l, p_w_h = sepal_width_range
    
    mask = (df['petal_width'] > low) & (df['petal_width'] < high) & (df['sepal_width'] > p_w_l) & (df['sepal_width'] < p_w_h) & (df['sepal_length'] > p_l_l) & (df['sepal_length'] < p_l_h)
    fig = px.scatter_3d(df[mask], x='sepal_length', y='sepal_width', z='petal_width', color='species')
    return fig
    
    
    
if __name__ == '__main__':
    app.run_server(debug=True)
    
    
