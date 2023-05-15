'''
如何在dash中处理图片 
'''

import plotly.express as px   
from dash import Dash, dcc, html, Input, Output, no_update, callback_context, MATCH, ALL 
import dash_daq as daq   
from skimage import data, draw  


import numpy as np  
import json 
from scipy import ndimage as ndi  


img = data.chelsea() 
fig = px.imshow(img)  
# fig.update_layout(dragmode='drawrect',
#                   newshape=dict(line_color='darkblue', fillcolor='cyan', opacity=0.5)
#                 )  

fig.update_layout(dragmode='drawclosedpath',
                  newshape=dict(line_color='darkblue', fillcolor='cyan', opacity=0.5)
                ) 

fig_hist = px.histogram(img.ravel()) 


config = {
    'modeBarButtonsToAdd': 
        ['drawline', 
         'drawopenpath', 
         'drawclosedpath', 
         'drawcircle', 
         'drawrect', 
         'eraseshape']
}


app = Dash(__name__)  
app.layout = html.Div([
    html.H3('Drag and draw annotation'),
    dcc.Graph(figure=fig, config=config),
    html.Hr(), 
    
    dcc.Markdown('''
                 ### dash callback trigger by dcc.Graph  when drawing annotations  
                 '''),
    dcc.Graph(id='graph', figure=fig, config=config),
    html.Pre(id='annotations-data'),
    html.Hr(),  
    
    dcc.Markdown('''
                 ### change the style of annotations  
                 '''),
    dcc.Graph(id='graph-style-annotations', figure=fig, config=config),
    html.Pre('Opacity of annotations'),
    dcc.Slider(id='opacity-slider', min=0, max=1, step=0.1, value=0.5),
    daq.ColorPicker(
        id='annotation-color-picker',
        label='color picker',
        value=dict(hex='#119DFF')
    ),
    html.Hr(), 
    
    dcc.Markdown('''
                 ### 矩形框 提取感兴趣区域
                 '''),
    html.H3('Drag a rectangel to show the histogram of the ROI'), 
    html.Div(
        [dcc.Graph(id='graph-pic', figure=fig, config=config),],
        style={'width': '50%', 'display': 'inline-block'}   
    ),
    html.Div(
        [dcc.Graph(id='graph-hist', figure=fig_hist, config=config),],
        style={'width': '50%', 'display': 'inline-block'}
    ),
    html.Hr(),
    
    html.H3('多边形 提取感兴趣区域'),
    dcc.Markdown('''
                 ### 对于多边形，我们需要以下几步：
                 - 我们从SVG路径中检索路径顶点的坐标
                 - 我们使用函数skimage.draw.polygon来获得被路径覆盖的像素的坐标
                 - 然后我们使用scipy.ndimage.binary_fill_holes函数将路径包围的像素设置为True
                 '''),
    html.Div(
        [dcc.Graph(id='graph-ploy', figure=fig),],
        style={'width': '50%', 'display': 'inline-block'}
    ),
    html.Div(
        [dcc.Graph(id='graph-ploy-hist', figure=fig_hist),],
        style={'width': '50%', 'display': 'inline-block'}   
    ),
    html.Hr(), 
    
    html.H3('修改形状, 解析relayoutData'),
    dcc.Markdown('''
        添加新形状时，relayoutData变量包含在所有布局形状的列表中
        也可以通过选择一个现有的形状，并单击模型栏中的“删除形状”按钮来删除形状
        一个已经存在的图形也可以进行修改       
    '''),
    html.H4('Draw a shape, then modify it'),
    dcc.Graph(id='graph-modify', figure=fig, config=config),
    dcc.Markdown('''Characteristics of the shape:'''),
    html.Pre(id='shape-data'),
    html.Hr(), 
    
        
    
    
    
])


# ==================== functions ====================
def path_to_indices(path):
    '''
    from svg path to numpy array of coordinates
    each row being  a (row, col) point  
    '''
    indices_str = [
        el.replace('M', '').replace('Z', '').split(',') for el in path.split('L') 
    ]
    
    return np.rint(np.array(indices_str, dtype=float)).astype(np.int)
    

def path_to_mask(path, shape):
    '''
    from svg path to a boolean array where all pixels enclosed by the path are True
    and the others pixels are False   
    '''
    cols, rows = path_to_indices(path).T  
    rr, cc = draw.polygon(rows, cols)
    mask = np.zeros(shape, dtype=bool) 
    mask[rr, cc] = True  
    mask = ndi.binary_fill_holes(mask)  
    return mask 



# ==================== callback ====================  
@app.callback(
    Output('annotations-data', 'children'),
    Input('graph', 'relayoutData'),
    prevent_initial_call=True 
)
def on_new_annotation(relayoutData):
    if 'shapes' in relayoutData:
        return json.dumps(relayoutData['shapes'], indent=2)
    else:
        return no_update   
    


@app.callback(
    Output('graph-style-annotations', 'figure'),
    Input('opacity-slider', 'value'),
    Input('annotation-color-picker', 'value'),
    prevent_initial_call=True
)
def on_style_annotations(opacity, color):
    fig = px.imshow(img)
    fig.update_layout(dragmode='drawrect',
                        newshape=dict(fillcolor=color['hex'], opacity=opacity)
                        )
    return fig  



@app.callback(
    Output('graph-hist', 'figure'),
    Input('graph-pic', 'relayoutData'),
    prevent_initial_call=True
)
def on_extract_roi(relayoutData):
    if 'shapes' in relayoutData:
        last_shape = relayoutData['shapes'][-1] 
        # shape coordingates are floats, we need to convert to ints for slicing  
        x0, y0 = int(last_shape['x0']), int(last_shape['y0'])
        x1, y1 = int(last_shape['x1']), int(last_shape['y1']) 
        roi = img[y0:y1, x0:x1]  
        return px.histogram(roi.ravel()) 
    else:
        return no_update 
        
        
        
@app.callback(
    Output('graph-ploy-hist', 'figure'),
    Input('graph-ploy', 'relayoutData'),
    prevent_initial_call=True
)
def on_extract_roi_poly(relayoutData):
    if "shapes" in relayoutData:
        last_shape = relayoutData["shapes"][-1]
        mask = path_to_mask(last_shape["path"], img.shape)
        return px.histogram(img[mask])
    else:
        return no_update



@app.callback(
    Output('shape-data', 'children'),
    Input('graph-modify', 'relayoutData'),
    prevent_initial_call=True
)
def on_modify_shape(relayoutData):
    for key in relayoutData:
        if 'shapes' in relayoutData:
            return json.dumps(f'{key}: {relayoutData[key]}', indent=2)
    else:
        return no_update



if __name__ == '__main__':
    app.run_server(debug=True) 
    
    