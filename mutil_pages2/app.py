import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import dash_bootstrap_components as dbc

  
  

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.4/dbc.min.css"
app = Dash(__name__, 
           meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
           external_stylesheets=[dbc.themes.CERULEAN, dbc_css], 
           use_pages=True)

server = app.server  

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})
app.scripts.config.serve_locally = True


app.title = 'spatialomics analysis platform'


navbar = dbc.NavbarSimple(
    [
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("联合分析", href="/combineanalysis")),
        dbc.NavItem(dbc.NavLink("About", href="/about")),
    ],
    brand="空间代谢组&空间转录组联合分析平台",
    brand_href="#",
    color="primary",
    dark=True,
    style={
        "height": "50px",
        'margin': '0px',
        'padding': '0px',
        'border': '0px'
        }
)

app.layout = dbc.Container(
    [
        dbc.Row(dbc.Col(navbar, width=12), class_name="d-flex"),
        dbc.Row(
            dbc.Col(
                    dash.page_container,
                    width=12,
                    )
                    # ,class_name="mh-100 d-flex justify-content-center"
                ),
        
        dbc.Row(
            html.Footer("2023 Bioinformatics Quest All Right Reserved.",className="d-flex justify-content-center")
            ,class_name="d-flex justify-content-center"
            )
    ], 
    fluid=True,
    # class_name="grid gap-0 row-gap-3"
)

if __name__ == "__main__":
    app.run_server(debug=True)


