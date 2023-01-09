from dash import Dash, html
import dash_bootstrap_components as dbc

from app.components import scatter_plot, weight_slider
from app.data.source import DataSource


def create_layout(app: Dash, data: DataSource) -> dbc.Container:
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
                        xs=12, lg=8,
                        children=[
                            scatter_plot.render(data, weights=[0, 0, 0, 0])
                        ]
                    ),
                    dbc.Col(
                        xs=12, lg=4,
                        children=[
                            weight_slider.render_two_inputs(app, data)
                        ]
                    )
                ]
            )
        ]
    )
