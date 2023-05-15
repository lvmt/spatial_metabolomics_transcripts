'''
genomic data  
chromosome data  
'''

import json 
import dash  
import dash_bio as dashbio
from dash import html, dcc, State
import urllib.request as urlreq  
from dash.dependencies import Input, Output  

import pandas as pd  


app = dash.Dash(__name__) 


# ======================= data ==============================
fastq_data = open('alignment_viewer_p53.fasta', 'r').read() 


needle_data = open('needle_PIK3CA.json').read()
needle_mdata = json.loads(needle_data) 

volcano_data = pd.read_csv('volcano_data1.csv')

circos_data = json.loads(open('circos_graph_data.json').read())
circos_layout_config = {
    "innerRadius": 100,
    "outerRadius": 200,
    "cornerRadius": 4,
    "labels": {
        "size": 10,
        "color": "#4d4d4d",
    },
    "ticks": {
        "color": "#4d4d4d",
        "labelColor": "#4d4d4d",
        "spacing": 10000000,
        "labelSuffix": "Mb",
        "labelDenominator": 1000000,
        "labelSize": 10,
    },
}


cluster_df = pd.read_csv('clustergram_brain_cancer.csv').set_index('ID_REF') 
columns = list(cluster_df.columns.values) 
rows = list(cluster_df.index) 

manhattan_df = pd.read_csv('manhattan_data.csv') 


HOSTED_GENOME_DICT = [
    {'value': 'mm10', 'label': 'Mouse (mm10)'},
    {'value': 'hg19', 'label': 'Human (hg19)'},
]

HOSTED_GENOME_TRACKS = {
    'mm10': {
        'range': {
            'contig': 'chr17',
            'start': 7571745,
            'stop': 7577544
        },
        'reference': {
            'label': 'mm10',
            'url': 'https://hgdownload.cse.ucsc.edu/goldenPath/mm10/bigZips/mm10.2bit'
        },
        'tracks': [
            {
                'viz': 'scale',
                'label': 'Scale',
            },
            {
                'viz': 'location',
                'label': 'Location',
            }
        ]
    },
    'hg19': {
        'range': {
            'contig': 'chr17',
            'start': 7571745,
            'stop': 7577544
        },
        'reference': {
            'label': 'hg19',
            'url': 'https://hgdownload.cse.ucsc.edu/goldenPath/hg19/bigZips/hg19.2bit'
        },
        'tracks': [
            {
                'viz': 'scale',
                'label': 'Scale',
            },
            {
                'viz': 'location',
                'label': 'Location',
            },
            {
                'viz': 'genes',
                'label': 'genes',
                'source': 'bigBed',
                'sourceOptions': {'url': 'https://www.biodalliance.org/datasets/ensGene.bb'}
            }
        ]
    }
}

# ======================= layout ==============================


app.layout = html.Div([
    html.H1('Dash Bio Alignment Viewer'),
    dashbio.AlignmentChart(
        id='my-default-alignment-viewer',
        data=fastq_data,
        height=900,
        tilewidth=30,
        colorscale='hydro',
    ),
    html.Div(id='alignment-viewer-output'),
    html.Hr(), 
    
    html.H1('Dash Bio NeedlePlot'), 
    dcc.Dropdown(
        id='default-needleplot-dropdown',
        options=[
            {'label': 'Show', 'value': 1},
            {'label': 'Hide', 'value': 0}
        ],
        clearable=False,
        multi=False,  
        value=1,
        style={'width': '50%'}
    ),
    dashbio.NeedlePlot(
        id='my-default-needleplot',
        mutationData=needle_mdata,
    ),
    html.Hr(),   
    
    html.H1('Dash Bio VolcanoPlot'),
    'Effect sizes',
    dcc.RangeSlider(
        id='volcano-effect-size-slider',
        min=-3,
        max=3,
        step=0.05,
        marks={i: {'label': str(i)} for i in range(-3, 4)},
        value=[-1, 1]
    ),
    'Genome-wide significance line',
    dcc.Slider(
        id='volcano-genome-wide-slider',
        min=0,
        max=5,
        step=0.05,
        marks={i: {'label': str(i)} for i in range(0, 6)},
        value=2.5
    ),
    html.Br(),
    html.Div(
        dcc.Graph(
            id='volcano-plot',
            figure=dashbio.VolcanoPlot(
                dataframe=volcano_data,
            )
        )
    ),
    html.Hr(), 
    
    html.H1('CIRCOS'),
    dashbio.Circos(
        id="my-dashbio-default-circos",
        layout=circos_data['GRCh37'],
        config=circos_layout_config,
        selectEvent={'0': 'hover', '1': 'click', '2': 'both'},
        tracks=[
            {   
                'type': 'CHORDS',
                'data': circos_data['chords'],
                'config': {
                    'tooltipContent': {
                        'source': 'source',
                        'sourceID': 'id',
                        'target': 'target',
                        'targetID': 'id',
                        'targetEnd': 'end'
                    }
                }
            }
        ]
    ),
    'Graph type: ',
    dcc.Dropdown(
        id="histogram-chords-default-circos",
        options=[
            {'label': 'CHORDS', 'value': 'CHORDS'},
            {'label': 'HISTOGRAM', 'value': 'HISTOGRAM'},
            {'label': 'LINE', 'value': 'LINE'},
            {'label': 'SCATTER', 'value': 'SCATTER'},
            {'label': 'STACK', 'value': 'STACK'},
            {'label': 'TEXT', 'value': 'TEXT'}
        ],
        value='CHORDS',
    ),
    'Event data: ',
    html.Div(id="default-circos-output"),
    html.Hr(),
    
    html.H1('cLUSTERGRAM'),
    'Rows to display: ',
    dcc.Dropdown(
        id='my-default-clustergram-input',
        options=[
            {'label': i, 'value': i} for i in rows
        ],
        value=rows[:10],
        multi=True
    ),
    
    html.Div(id='my-default-clustergram-output'), 
    html.Hr(), 
    
    html.H1('manhattan plot'), 
    'Threshold value: ',
    dcc.Slider(
        id='manhattan-threshold-slider',
        min=1,
        max=10,
        marks={
            i: {'label': str(i)} for i in range(1, 10)
        },
        value=6,
    ),
    html.Br(),
    html.Div(
        dcc.Graph(
            id='manhattan-plot',
            figure=dashbio.ManhattanPlot(
                dataframe=manhattan_df,
            )
        )
    ),
    html.Hr(),
    
    html.H1('Pileup'),
    dcc.Loading(id='default-pileup-container'),
    html.Hr(),
    html.P('select a genome to display below'),
    dcc.Dropdown(
        id='default-pileup-genome-select',
        options=HOSTED_GENOME_DICT,
        value='hg19', 
    )
])  



# ======================= callback ============================== 
@app.callback(
    Output('alignment-viewer-output', 'children'),
    Input('my-default-alignment-viewer', 'eventDatum')
)
def update_output(value):
    if value is None:
        return 'NO DATA'  
    else:
        return str(value) 
    
    
@app.callback(
    Output('my-default-needleplot', 'rangeSlider'),
    Input('default-needleplot-dropdown', 'value')
)
def update_needleplot(value):
    return True if str(value) == '1' else False 
    


@app.callback(
    Output('volcano-plot', 'figure'),
    Input('volcano-effect-size-slider', 'value'),
    Input('volcano-genome-wide-slider', 'value')
)
def update_volcanoplot(effect_size, genome_wide):
    return dashbio.VolcanoPlot(
        dataframe=volcano_data,
        genomewideline_value=genome_wide, 
        effect_size_line=effect_size,
        highlight_color='#119DFF',
        col='#2A3F5F'  
    )
    
    
    
@app.callback(
    Output("default-circos-output", "children"),
    Input("my-dashbio-default-circos", "eventDatum"),
)
def update_output(value):
    if value is not None:
        return [html.Div("{}: {}".format(v.title(), value[v])) for v in value.keys()]
    return "There are no event data. Hover over a data point to get more information."


@app.callback(
    Output("my-dashbio-default-circos", "tracks"),
    Input("histogram-chords-default-circos", "value"),
    State('my-dashbio-default-circos', 'tracks'),
)
def update_circos_graph(value, current):
    if value == "histogram":
        current[0].update(data=circos_data["histogram"], type="HISTOGRAM")

    elif value == "chords":
        current[0].update(
            data=circos_data["chords"],
            type="CHORDS",
            config={
                "tooltipContent": {
                    "source": "source",
                    "sourceID": "id",
                    "target": "target",
                    "targetID": "id",
                    "targetEnd": "end",
                }
            },
        )
    return current
    
    
    
@app.callback(
    Output('my-default-clustergram-output', 'children'),
    Input('my-default-clustergram-input', 'value')
)
def update_clustergram(rows):
    if len(rows) < 2:
        return 'Please select at least two rows'
    
    return dcc.Graph(
        figure=dashbio.Clustergram(
            data=cluster_df.loc[rows].values,
            row_labels=rows,
            color_threshold={'row': 250, 'col': 700},
            height=800,
            width=800,
            hidden_labels=['row'],
            color_map=[
                [0.0, '#636EFA'],
                [0.25, '#AB63FA'],
                [0.5, '#FFFFFF'],
                [0.75, '#E763FA'],
                [1.0, '#EF553B']
            ],
            line_width=2,
        )
    )
    
    
    
@app.callback(
    Output('manhattan-plot', 'figure'),
    Input('manhattan-threshold-slider', 'value')
)
def update_manhattan(threshold):
    return dashbio.ManhattanPlot(
        dataframe=manhattan_df,
        genomewideline_value=threshold,
    )
    
    
    
@app.callback(
    Output('default-pileup-container', 'children'),
    Input('default-pileup-genome-select', 'value')
)
def update_pileup(genome):
    if HOSTED_GENOME_TRACKS.get(genome) is None:
        raise Exception('No tracks for genemo {}'.format(genome))
    
    return (
        html.Div([
            dashbio.Pileup(
                id='pileup-default',
                range=HOSTED_GENOME_TRACKS[genome]['range'],
                reference=HOSTED_GENOME_TRACKS[genome]['reference'],
                tracks=HOSTED_GENOME_TRACKS[genome]['tracks'],
            )
        ])
    )
    
    

if __name__ == '__main__':
    app.run_server(debug=True) 
    
    
    