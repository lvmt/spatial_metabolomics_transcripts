'''
combine holoviews and dash to show the image and draw the annotation 

link_selection  

HoloViews对Dash用户来说特别方便的一个特性是能够自动链接图形之间的选择，而不需要手动定义任何回调函数。
'''
# -*- coding: utf-8 -*-
import dash
from dash import html
from plotly.data import iris

import holoviews as hv
from holoviews import opts
from holoviews.plotting.plotly.dash import to_dash

# Load dataset
df = iris()
dataset = hv.Dataset(df)

# Build selection linking object
selection_linker = hv.selection.link_selections.instance()
scatter = selection_linker(
    hv.Scatter(dataset, kdims=["sepal_length"], vdims=["sepal_width"])
)
hist = selection_linker(
    hv.operation.histogram(dataset, dimension="petal_width", normed=False)
)

# Use plot hook to set the default drag mode to box selection
def set_dragmode(plot, element):
    fig = plot.state
    fig['layout']['dragmode'] = "select"
    if isinstance(element, hv.Histogram):
        # Constrain histogram selection direction to horizontal
        fig['layout']['selectdirection'] = "h"

scatter.opts(opts.Scatter(hooks=[set_dragmode]))
hist.opts(opts.Histogram(hooks=[set_dragmode]))

app = dash.Dash(__name__)
components = to_dash(
    app, [scatter, hist], reset_button=True
)

app.layout = html.Div(components.children)

if __name__ == "__main__":
    app.run_server(debug=True)
