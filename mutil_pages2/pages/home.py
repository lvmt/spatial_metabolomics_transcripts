import dash
from dash import html, dcc
import dash_bootstrap_components as dbc


# 每个页面都需要用dash.register_page(name, path='/') 声明是一个页面，path='/'设置路径为根路径
dash.register_page(__name__, path='/')

carousel = dbc.Carousel(
    items=[
        {
            "key": "1",
            "src": "/static/images/st-logo.resize.jpg",
            "header": "With header ",
            "caption": "and caption",
        },
        {
            "key": "2",
            "src": "/static/images/sm-logo.resize.jpg",
            "header": "",
            "caption": "This slide has a caption only",
        },
    ],
    # style={"height": "50vh"},
    # class_name="vw-10",
    # style={"maxWidth": "600px"},
    ride="carousel"
)


def make_card(txt, img, href):
    _card = dbc.Card(
        [
            # dbc.CardHeader(header, style={'textAlign':'center'}),
            dbc.CardImg(src="/static/images/"+img, className="img-fluid rounded-start col-md-2"),
            dbc.CardBody(
                [
                    html.P(txt, style={'textAlign':'center'}),
                    dbc.Button("go to analysis", color="primary",href=href, class_name="d-flex justify-content-center p-3"),
                ],
            ),
        ],
        
        className="border-0 bg-transparent g-col-3",
        # style={"width": "12rem", 'height':'20rem'},
    ) 
    
    return _card



layout = dbc.Container(
    [
        dbc.Row(carousel, class_name="h-10"),
        html.Br(),
        html.Hr(style={"border-top": "1px solid #8c8b8b"}),
        dbc.Row(
            dbc.CardGroup(
                [
                    make_card(txt="C. elegans survival analysis",img="1.jpg",href='https://bioquest.shinyapps.io/cesa'),
                    make_card(txt="iris scatter",img="scatter.logo.jpg",href="/iris"),
                    make_card(txt="iris cluster",img="cluster.logo.png",href="/iris"),
                    make_card(txt="iris",img="1.jpg",href="/iris"),
                    
                ],
                class_name = "grid gap-3"
            ),
            # class_name="d-flex justify-content-center"
        ),
        dbc.Row(
            [
            dbc.Col(
                make_card(txt="iris hist",img="1.jpg",href="/iris"),width=3,
            )
            ]
        )
    ],
    ) 
