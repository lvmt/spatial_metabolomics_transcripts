from dash import Dash, dcc, html, Input, Output, ctx 
import pandas as pd  
import plotly.express as px  


filepath = "https://raw.githubusercontent.com/plotly/datasets/master/volcano_db.csv"
df = pd.read_csv(filepath, encoding='latin')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css'] 

app = Dash(__name__, external_stylesheets=external_stylesheets) 
app.layout = html.Div(
    [
        html.Header(
            'Geographic Visualization of Volcanoes',
            style={'textAlign': 'center', 'fontSize': 30}
        ),
        html.Div(
            'Minimum Volcano Height', style={'fontSize': 20}
        ),
        'Meters',
        dcc.Input(id='meter', value=2000, type='number', step=1),
        'Feet',
        dcc.Input(id='feet', value=6561, type='number'),
        dcc.Graph(id='map') 
        
    ],
    style={'margin': '10', 'width': 800} 
)


@app.callback(
    Output('meter', 'value'),
    Output('feet', 'value'),
    Output('map', 'figure'),
    Input('meter', 'value'),
    Input('feet', 'value')
)
def update_figure(meter, feet):
    if ctx.triggered_id == "meter":
        feet = None if meter is None else round((float(meter) * 3.28084), 0)
    else:
        meter = None if feet is None else round((float(feet) / 3.28084), 1)
        
    fig = px.scatter_geo(
        data_frame=df.loc[df['Elev'] >= meter],
        lat='Latitude',
        lon='Longitude',
        size='Elev',
        hover_name='Volcano Name',
        projection='natural earth',
    )
    
    return meter, feet, fig 



if __name__ == '__main__':
    app.run_server(debug=True)
    
    