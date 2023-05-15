from dash import Dash, dcc, html, Input, Output
import plotly.express as px  
import pandas as pd  
import dash_daq_demo as daq 
import plotly.io as pio  
import time  


df = px.data.gapminder()
df = df.loc[df['year'] == 1952] 

# set the template to ggplot2  
# here are all the default templates 
# ggplot2, seaborn, simple_white, plotly, plotly_white, plotly_dark,
pio.templates.default = 'ggplot2' 

app = Dash(__name__) 

app.layout = html.Div(
    [
        html.H2('Interactive Bar Colour Control'),
        dcc.Loading(dcc.Graph(id='graph'), type='circle'),
        daq.ColorPicker(
            id='color',
            label='Color of Bars',
            size=164,
            value=dict(hex='#119dff')
        )
    ]
)


@app.callback(
    Output('graph', 'figure'),
    Input('color', 'value')
)
def update_points_color(color):
    fig = px.histogram(
        df,
        x='lifeExp',
        labels={'lifeExp': 'Life Expectancy'},
        title='Life Expectancy Distribution',
        nbins=23,
    )
    
    fig.update_layout(yaxis_title='Count')
    fig.update_traces(markder=dict(color=color['hex']))
    time.sleep(1)
    
    return fig  


if __name__ == '__main__':
    app.run_server(debug=True)