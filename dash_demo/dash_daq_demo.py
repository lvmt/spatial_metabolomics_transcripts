from dash import Dash, html, Input, Output, dcc  
import dash_daq as daq

app = Dash(__name__)

app.layout = html.Div([
    
    dcc.Markdown('''
                 ### Dash DAQ: BooleanSwitch
                 '''),
    daq.BooleanSwitch(id='our-boolean-switch', 
                      on=False, 
                      color="#9B51E0",
                      label='Default label',
                      labelPosition='top'
                      ),
    html.Div(id='boolean-switch-result'),
    html.Hr(),
    
    dcc.Markdown('''
                 ### color picker
                 '''),
    daq.ColorPicker(
        id='my-color-picker',
        label='color picker',
        value=dict(hex='#119DFF')
    ),
    html.Div(id='color-picker-result'),
    html.Hr(), 
    
    dcc.Markdown('''
                 ### numeric input 
                 '''),
    daq.NumericInput(
        id='my-numeric-input',
        value=0,
        size=120,
        max=100, 
        min=20,
    ),
    html.Div(id='numeric-input-result'),
    html.Hr(),  
    
    
])


# ============================= Callback =============================
@app.callback(
    Output('boolean-switch-result', 'children'),
    Input('our-boolean-switch', 'on')
)
def update_output(on):
    return f'The switch is {on}.'



@app.callback(
    Output('color-picker-result', 'children'),
    Input('my-color-picker', 'value')
)
def update_color(value):
    return f'The selected color is {value["hex"]}.'  




if __name__ == '__main__':
    app.run_server(debug=True)
