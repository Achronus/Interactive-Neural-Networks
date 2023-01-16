from dash import Dash, html
import dash_bootstrap_components as dbc

from app.components import scatter_plot, nn_slider
from app.data import ids
from app.data.source import DataSource


def create_layout(app: Dash, data: DataSource) -> dbc.Container:
    """
    Creates the Dash application layout and returns it.

    :param app: (Dash) an existing Dash application
    :param data: (DataSource) a data source object containing data

    :return: a dash dbc.Container containing the applications layout
    """
    return dbc.Container(
        className="app-div container mt-4 mb-4",
        children=[
            dbc.Row(dbc.Col(xs=12, children=[
                html.H1(app.title),
                html.Hr()
            ])),
            dbc.Row(
                children=[
                    dbc.Col(
                        id=ids.SCATTER_PLOT1_CONTAINER,
                        className=['align-self-center'],
                        xs=12, lg=8,
                        children=[
                            scatter_plot.render(
                                data,
                                weights=ids.SIMPLE_NN_START_WEIGHTS,
                                biases=ids.SIMPLE_NN_START_BIASES
                            )
                        ]
                    ),
                    dbc.Col(
                        xs=12, lg=4,
                        children=[
                            nn_slider.render_simple_params(
                                app, data,
                                weights=ids.SIMPLE_NN_START_WEIGHTS,
                                biases=ids.SIMPLE_NN_START_BIASES
                            )
                        ]
                    )
                ]
            )
        ]
    )
