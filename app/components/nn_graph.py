from dash import Dash, html
import dash_cytoscape as cyto

from dash.dependencies import Input, Output
from app.data import ids

DEFAULT_STYLESHEET = [
    {
        'selector': 'node',
        'style': {
            'label': 'data(label)'
        }
     },
    {
        'selector': 'edge',
        'style': {
            'label': 'data(label)',
            'curve-style': 'bezier'
        }
    },
    {
        'selector': 'data(label)',
        'style': {
            'color': 'white',
            'font-size': 12
        }
    }
]

NO_HIDDEN_NODES = [
    {
        'data': {
             'id': 'input_1',
             'label': f'Input ₁'
         },
        'position': {
            'x': 50,
            'y': 50
        },
        'style': {
            'textValign': 'center',
            'textHalign': 'left',
            'textMarginX': '-5px'
        }
    },
    {
        'data': {
            'id': 'input_2',
            'label': 'Input ₂'
        },
        'position': {
            'x': 50,
            'y': 200
        },
        'style': {
            'textValign': 'center',
            'textHalign': 'left',
            'textMarginX': '-5px'
        }
    },
    {
        'data': {
            'id': 'output_1',
            'label': 'Output ₁'
        },
        'position': {
            'x': 600,
            'y': 50
        },
        'style': {
            'textValign': 'center',
            'textHalign': 'right',
            'textMarginX': '5px'
        }
    },
    {
        'data': {
            'id': 'output_2',
            'label': 'Output ₂'
        },
        'position': {
            'x': 600,
            'y': 200
        },
        'style': {
            'textValign': 'center',
            'textHalign': 'right',
            'textMarginX': '5px'
        }
    }
]

NO_HIDDEN_EDGES = [
    {
        'data': {
            'source': 'input_1',
            'target': 'output_1',
            'label': 'Weight₁,₁',
        },
        'style': {
            'textMarginY': '-10px',
            'textMarginX': '-180px'
        }
    },
    {
        'data': {
            'source': 'input_2',
            'target': 'output_1',
            'label': 'Weight₂,₁',
        },
        'style': {
            'textMarginY': '40px',
            'textMarginX': '-175px',
            'textRotation': '-15deg'
        }
    },
    {
        'data': {
            'source': 'input_1',
            'target': 'output_2',
            'label': 'Weight₁,₂',
        },
        'style': {
            'textMarginY': '-35px',
            'textMarginX': '-95px',
            'textRotation': '15deg'
        }
    },
    {
        'data': {
            'source': 'input_2',
            'target': 'output_2',
            'label': 'Weight₂,₂',
        },
        'style': {
            'textMarginY': '-10px',
            'textMarginX': '-100px'
        }
    }
]


def _set_node_edge_highlight_styles(edge: dict, node: dict, selector_to: str, selector_from: str) -> list[dict, ...]:
    """Helper function to dynamically add styles to nodes."""
    stylesheet = []
    if selector_to == node['data']['id']:
        stylesheet.append({
            'selector': f'node[id="{selector_from}"]',
            'style': {
                'background-color': ids.HIGHLIGHT_COLOUR
            }
        })
        stylesheet.append({
            'selector': f'edge[id="{edge["id"]}"]',
            'style': {
                'line-color': ids.HIGHLIGHT_COLOUR
            }
        })
    return stylesheet


def render_simple_nn_no_hidden(app: Dash) -> html.Div:
    @app.callback(
        Output(ids.SIMPLE_NN_NO_HIDDEN_GRAPH, 'stylesheet'),
        Input(ids.SIMPLE_NN_NO_HIDDEN_GRAPH, 'tapNode')
    )
    def highlight_node_edges(node) -> list[dict, ...]:
        if not node:
            return DEFAULT_STYLESHEET

        stylesheet = [
            {
                'selector': f'node[id="{node["data"]["id"]}"]',
                'style': {
                    'background-color': ids.HIGHLIGHT_COLOUR,
                    'border-color': ids.HIGHLIGHT_COLOUR
                }
            }
        ]

        for edge in node['edgesData']:
            stylesheet += _set_node_edge_highlight_styles(edge, node, edge['source'], edge['target'])
            stylesheet += _set_node_edge_highlight_styles(edge, node, edge['target'], edge['source'])

        return DEFAULT_STYLESHEET + stylesheet

    return html.Div(
        className='mt-3 mb-3',
        children=[
            cyto.Cytoscape(
                id=ids.SIMPLE_NN_NO_HIDDEN_GRAPH,
                userPanningEnabled=False,
                autolock=True,
                elements=NO_HIDDEN_NODES + NO_HIDDEN_EDGES,
                layout={'name': 'preset'},
                style={'width': '100%', 'height': '300px'},
                stylesheet=DEFAULT_STYLESHEET
            )
        ])
