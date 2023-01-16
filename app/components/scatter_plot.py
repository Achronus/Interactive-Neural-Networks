import numpy as np

from dash import dcc, html
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from ..data import ids
from ..data.generate import DataSchema
from ..data.source import DataSource
from ..models.classifier import SimpleNeuralNetwork


def render(source: DataSource, weights: list[float], biases: list[float]) -> html.Div:
    """
    Displays a scatter plot, overlaid with a heatmap.

    :param source: (DataSource) a data source object containing data
    :param weights: (list[float]) a list of neural network weights
    :param biases: (list[float]) a list of neural network biases

    :return: a dash html.Div containing the scatter plot
    """
    fig = make_subplots(rows=1, cols=1)
    fig = _set_background(fig, source, weights, biases)
    fig = _set_scatter(fig, source)
    return html.Div(dcc.Graph(figure=fig, config={'staticPlot:': True}), id=ids.SCATTER_PLOT)


def _set_scatter(fig: go.Figure, source: DataSource) -> go.Figure:
    """
    Creates a scatter plot from data supplied to a DataSource object.

    :param fig: (go.Figure) an existing set of subplots
    :param source: (DataSource) a data source object containing data

    :return: a dash graph object figure containing the scatter plot
    """
    colours = {ids.LABEL_ONE: ids.POSITIVE_COLOUR, ids.LABEL_TWO: ids.NEGATIVE_COLOUR}
    filtered_data = source.filter(x=source.all_x, y=source.all_y, labels=source.all_labels)

    scatter = px.scatter(filtered_data.data, x=DataSchema.X_AXIS, y=DataSchema.Y_AXIS, color=DataSchema.LABELS,
                         color_discrete_map=colours, template='none')
    scatter.update_traces(marker_size=10)

    fig.update_layout(
        plot_bgcolor=ids.BG_COLOUR,
        paper_bgcolor=ids.BG_COLOUR,
        legend=dict(bgcolor=ids.BG_COLOUR, title=None, orientation="h", y=1, x=0.5, yanchor='bottom', xanchor='center'),
        font_color='white'
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    fig.add_traces(list(scatter.select_traces()), 1, 1)
    return fig


def _set_background(fig: go.Figure, source: DataSource, weights: list[float], biases: list[float]) -> go.Figure:
    """
    Applies a heatmap over the scatter plot, displaying the networks predictions as an overlaid coloured.

    :param fig: (go.Figure) an existing set of subplots
    :param source: (DataSource) a data source object containing data
    :param weights: (list[float]) a list of neural network weights
    :param biases: (list[float]) a list of neural network biases

    :return: a dash graph object figure containing the scatter plot
    """
    clf = SimpleNeuralNetwork(weights, biases)

    # Create a mesh to plot
    h = .02  # step size
    threshold = 0.2
    X = np.asarray(source.x_and_y)
    x_min, x_max = X[:, 0].min() - threshold, X[:, 0].max() + threshold
    y_min, y_max = X[:, 1].min() - threshold, X[:, 1].max() + threshold
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))

    Z = clf.calc(np.c_[xx.ravel(), yy.ravel()])
    Z = np.asarray(Z).reshape(xx.shape)
    y_ = np.arange(y_min, y_max, h)

    plot = go.Heatmap(x=xx[0], y=y_, z=Z, showscale=False, colorscale=[[0, ids.POSITIVE_COLOUR],
                                                                       [0.5, ids.NEGATIVE_COLOUR]], opacity=0.4)
    fig.add_trace(plot, 1, 1)
    return fig
