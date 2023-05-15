import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__)

card_about = dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.CardImg(
                        src="/static/images/profile.jpg",
                        className="img-fluid rounded-start",
                    ),
                    className="col-md-6 img-thumbnail mx-auto d-block",
                ),
                dbc.Col(
                    dbc.CardBody(
                        [
                            html.P("hahahh"),
                            html.P("TEL&Wechat: +86 XXXXXXX"),
                            html.P("Email: XXXXXXX@qq.com"),
                        ],
                        class_name = "font-weight-bold",
                        style={"font-size": "17px"},
                    ),
                    className="col-md-6 d-flex align-items-center",
                ),
            ],
            className="",
            
        )
    ],
    className="mb-3 w-90",
    style={"maxWidth": "600px"},
    outline=True 
)

md_text = open("static/about.md", encoding='utf-8').readlines()

layout = dbc.Container(
    [
        html.Br(),
        card_about,
        dcc.Markdown(md_text)
    ]    
    )
