# 展示dash 核心组件的用法 
import dash  
from dash import Dash, html, dcc, Input, Output, State, dash_table 


import json 
import base64 
import io  
import pandas as pd   
import datetime   
from datetime import date  
import plotly.express as px  



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']   
df_iris = px.data.iris()  

app = Dash(__name__, external_stylesheets=external_stylesheets)  


app.layout = html.Div(
    [
        dcc.Dropdown(['new york city', 'montreal', 'san francisco'], 'montreal', id='demo-dropdown'),
        html.Div(id='dd-output-container'),
        html.Br(),
        
        dcc.Dropdown(['new york city', 'montreal', 'san francisco'], 'montreal', multi=True), 
        html.Br(),
        
        html.Label('Slider'),
        dcc.Slider(-5, 10, 1, value=-3, id='my-slider'),
        # min, max, step是最开始的3个位置参数 
        html.Br(),
        
        dcc.Slider(-5, 10, 1, value=-3, marks={i: 'Label {}'.format(i) if i == 1 else str(i) for i in range(-5, 7)}),
        html.Br(), 
        
        # 关掉marks   
        dcc.Slider(-5, 10, 1, value=-3, marks=None),
        html.Br(),  
        
        # tooltip
        dcc.Slider(-5, 10, 1, value=-3, marks=None, tooltip={'always_visible': True, 'placement': 'bottom'}),
        html.Br(),
        
        # RangeSlider  
        dcc.RangeSlider(-5, 10, 1, value=[-3, 7], marks=None, tooltip={'always_visible': True, 'placement': 'bottom'}, id='my-range-slider'),
        html.Br(),
        
        # Input 
        dcc.Input(placeholder='enter a value...', type='text', value='', id='my-input'),
        html.Br(),  
        
        # debounce delays the input processing until the user stops typing for a certain amount of time  
        html.I('try typing in input 1 and 2, and oberseve how debounce affects the callbacks'),
        html.Br(),
        dcc.Input(id='input-1', type='text', placeholder='', style={'marginRight': '10px'}),
        dcc.Input(id='input-2', type='text', placeholder='', debounce=True),
        html.Div(id='output'),
        html.Br(),        
        
        # number input  
        dcc.Input(id='my-input2', type='number', min=0, max=10, step=0.5, value=5),
        html.Br(),  
        
        # Textarea  
        dcc.Textarea(placeholder='Enter a value...', value='This is a TextArea component', style={'width': '100%'}),
        html.Br(), 
        
        # checkboxes  
        dcc.Checklist(['New York City', 'Montreal', 'San Francisco'], ['Montreal'], inline=True),
        html.Br(),  
        
        # RadioItems  
        dcc.RadioItems(['New York City', 'Montreal', 'San Francisco'], 'Montreal', inline=True),
        html.Br(),
        
        # date picker single 
        dcc.DatePickerSingle(
            id='date-picker-single',
            date=date(1997, 5, 10)
            ),
        html.Br(),
          
        # date picker range  
        dcc.DatePickerRange(
            id='date-picker-range',
            start_date=date(1997, 5, 3),
            end_date_placeholder_text='Select a date!' 
        ),
        html.Br(), 
        
        # markdown   
        dcc.Markdown('''
                     ### 三级标题
                     dash components [dash components](https://dash.plot.ly/dash-core-components) 
                     it includes a set of pre-built components like dropdown, slider, textbox, graph etc. 
                     '''),
        html.Br(),
        
        # upload component  dcc.upload 'content is a base64 encoded string' 
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center'
            },
            multiple=True 
        ),
        html.Div(id='output-data-upload'),
        html.Br(),
        
        # display upload images  
        dcc.Markdown('''### 展示上传图片'''),
        dcc.Upload(
            id='upload-image',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center' 
            },
            multiple=True
        ),
        html.Div(id='output-image-upload'),
        html.Br(), 
        
        # 不同样式的上传
        dcc.Upload(html.Button('upload file')),
        html.Hr(),
        
        dcc.Upload(html.A('upload file')),
        html.Hr(), 
        
        ## download component   
        dcc.Markdown('''### 下载组件'''), 
        html.Button('Download File', id='btn'), 
        dcc.Download(id='download-text-index'),
        html.Hr(),
        
        # download content as strings  
        html.Button('Download File2', id='btn2'),
        dcc.Download(id='download-text2'),
        html.Hr(), 
        
        # download a dataframe as a csv file  
        html.Button('Download File3', id='btn3'),
        dcc.Download(id='download-csv3'),
        html.Hr(), 
        
        # download a dataframe as a excel file  
        html.Button('Download File4', id='btn4'),
        dcc.Download(id='download-excel4'),
        html.Hr(),  
        
        # download images   
        html.Button('Download File5', id='btn5'),
        dcc.Download(id='download-image5'),
        html.Hr(),
        
        # tabs 选项卡 
        dcc.Tabs(
                    id='tabs', 
                    value='tabl-1', 
                    children=[
                        dcc.Tab(label='Tab one', value='tab-1'),
                        dcc.Tab(label='Tab two', value='tab-2'),
                        dcc.Tab(label='Tab three', value='tab-3')
                    ]
                ),
        html.Div(id='tabs-content'),
        html.Hr(), 
        
        # Graph 和 开源的plotly.js图表库相同 
        dcc.Graph(
            figure=px.scatter(df_iris, x='sepal_width', y='sepal_length', color='species')
        ),
        html.Hr(),
        
        # store： 可以用于将数据存储在浏览器的本地存储中，以便在浏览器会话之间共享数据。  
        dcc.Markdown('''### store
                    memory: default, keep the data as long as the page is not refreshed.  
                    local: keep the data until it is manually cleared.
                    session: keep the data until the browser tab is closed. 
                    **for local/session, the data is serialized as json when stored**
                      '''),
        html.Hr(),
        
        dcc.Store(id='my-store'),
        dcc.RadioItems(['NYC', 'MTL', 'SF'], 'NYC', id='my-store-input'),
        html.Div(id='current-store')
        
        
        
    ]
)



# ================ some functions ==================
def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')  
    
    decode = base64.b64decode(content_string)   
    try:
        if 'csv' in filename:
            df = pd.read_csv(io.StringIO(decode.decode('utf-8')))
        elif 'xls' in filename:
            df = pd.read_excel(io.BytesIO(decode))
        else:
            df = pd.read_csv(io.StringIO(decode.decode('utf-8')), sep='\t')
    except Exception as e:
        print(e)
        return html.Div(['There was an error processing this file.'])  
    
    return html.Div([
        html.H5(filename),
        # html.H6(datetime(date)),
        
        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns]
        ),
        
        html.Hr(),
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={'whiteSpace': 'pre-wrap', 'wordBreak': 'break-all'})
    ])
    
        

def parse_image(contents, filename, date):
    return html.Div([
        html.H5(filename),
        
        # html images accept base64 encoded strings in the same format 
        # that is supplied by the upload component  
        html.Img(src=contents), 
        html.Hr(), 
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={'whiteSpace': 'pre-wrap', 'wordBreak': 'break-all'})
    ])
    

# ====================== callbacks ======================   

@app.callback(
    Output('output', 'children'),
    Input('input-1', 'value'),
    Input('input-2', 'value')
)
def update_output(input1, input2):
    return 'Input 1 is "{}" and Input 2 is "{}"'.format(input1, input2) 



@app.callback(
    Output('output-data-upload', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('upload-data', 'last_modified')
)
def update_upload_file(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)
        ]
        return children 
    


@app.callback(
    Output('output-image-upload', 'children'),
    Input('upload-image', 'contents'),
    State('upload-image', 'filename'),
    State('upload-image', 'last_modified')
)
def update_upload_image(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_image(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)
        ]
        return children
    


@app.callback(
    Output('download-text-index', 'data'),
    Input('btn', 'n_clicks'),
)
def download_text(n_clicks):
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate
    else:
        return dict(content='some text content', filename='my-file.txt')
    

@app.callback(
    Output('download-text2', 'data'),
    Input('btn2', 'n_clicks'),
    prevent_initial_call=True
)
def download_text2(n_clicks):
    return dict(content='some text content', filename='my-file.txt')


df = pd.DataFrame({"a": [1, 2, 3, 4], "b": [2, 1, 5, 6], "c": ["x", "x", "y", "y"]})
@app.callback(
    Output('download-csv3', 'data'),
    Input('btn3', 'n_clicks'),
    prevent_initial_call=True
)
def download_csv3(n_clicks):
    return dcc.send_data_frame(df.to_csv, "mydf.csv")


@app.callback(  
    Output('download-excel4', 'data'),
    Input('btn4', 'n_clicks'),
    prevet_initial_call=True        
)
def download_excel4(n_clicks):
    return dcc.send_data_frame(df.to_excel, "mydf.xlsx", sheet_name="Sheet_name_1")



@app.callback(
    Output('download-image5', 'data'),
    Input('btn5', 'n_clicks'),
    prevent_initial_call=True 
)
def download_image5(n_clicks):
    return dcc.send_file('assets/plotly_logo.png')


@app.callback(
    Output('tabs-content', 'children'),
    Input('tabs', 'value')
)
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.H3('Tab content 1')
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Tab content 2')
        ])
    elif tab == 'tab-3':
        return html.Div([
            html.H3('Tab content 3')
        ])
        


# =================== store =================== 
@app.callback(
    Output('my-store', 'data'),
    Input('my-store-input', 'value')
)
def update_store(value):
    return value


@app.callback(
    Output('current-store', 'children'),
    Input('my-store', 'modified_timestamp'),
    State('my-store', 'data')
)
def display_store_info(timestamp, data):
    return f"The store currently contains {data} and the modified timestamp is {timestamp}"
    




if __name__ == '__main__':
    app.run_server(debug=True) 
    
    
    