import dash  
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc  
from dash.dependencies import Input, Output  


# from pages.home import home_page 
# from pages.plot_demo import plot_page   


app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SPACELAB])  


app.layout = html.Div([
    html.H1('Multi-page Dash App', style={"textAlign": "center"}, className="bg-primary text-white p-2"), 
    html.Div([
        
    ]),
    
    html.Div([
        html.Div(
            dcc.Link(f'{page["name"]}', href=page['relative_path']), 
                    style={'margin': '2px', 
                           'padding': '2px',
                            'border': '1px solid #ddd',
                            'display': 'inline-block',
                            'textDecoration': 'none' 
                            }
            ) 
         for page in dash.page_registry.values() 
    ]),
    html.Hr(),
    
    dash.page_container 
    
])



if __name__ == '__main__':
    app.run_server(debug=True) 