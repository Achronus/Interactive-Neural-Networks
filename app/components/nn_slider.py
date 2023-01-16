from dataclasses import dataclass
import itertools

from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from app.components import scatter_plot
from app.data import ids
from app.data.source import DataSource


@dataclass
class WeightSlider:
    """
    A data class for creating a custom slider with default values.

    :param id: (str) a string representing the name of the slider
    :param min: (float) the minimum value of the slider. Default is -1
    :param max: (float) the maximum value of the slider. Default is 1
    :param step: (float) the movement size of the slider. Default is 0.1
    :param value: (float) the starting value of the slider. Default is 0
    """
    id: str
    min: float = -1
    max: float = 1
    step: float = 0.1
    value: float = 0

    def create(self) -> dcc.Slider:
        return dcc.Slider(
            min=self.min, max=self.max, step=self.step, value=self.value,
            id=f'{ids.WEIGHT_SLIDER}-{self.id}',
            marks={
                self.min: {'label': str(self.min)},
                self.value: {'label': str(self.value)},
                self.max: {'label': str(self.max)}
            },
            tooltip={"placement": "bottom", "always_visible": True}
        )


def render_simple_params(app: Dash, data: DataSource) -> html.Div:
    """
    Creates weight slider data for a neural network containing two inputs and two outputs (no hidden layers) and
    uses a callback to update its corresponding scatter plot when sliders are changed.

    :param app: (Dash) an existing Dash application
    :param data: (DataSource) a data source object containing data

    :return: a dash html.Div containing weight sliders
    """
    input_count = 2
    indices = [i for i in range(1, input_count+1)] * input_count
    indices.sort()  # [1, 1, 2, 2]

    slider_titles = [html.H6(f'w{i}_{idx}') for _, group in itertools.groupby(indices) for idx, i in enumerate(group, start=1)]
    sliders = [WeightSlider(id=f'{i}').create() for i in range(len(slider_titles))]
    weight_content = list(itertools.chain.from_iterable(zip(slider_titles, sliders)))

    @app.callback(
        Output(ids.SCATTER_PLOT, "children"),
        [
            Input(f'{ids.WEIGHT_SLIDER}-0', "value"),
            Input(f'{ids.WEIGHT_SLIDER}-1', "value"),
            Input(f'{ids.WEIGHT_SLIDER}-2', "value"),
            Input(f'{ids.WEIGHT_SLIDER}-3', "value")
        ]
    )
    def update_plot(w1: float, w2: float, w3: float, w4: float) -> html.Div:
        return scatter_plot.render(data, weights=[w1, w2, w3, w4])

    return html.Div(
        id=ids.WEIGHTS_CONTAINER,
        className=['mt-5'],
        children=[
            html.H5('Weights'),
            html.Div(id=ids.WEIGHT_SLIDER_CONTAINER, children=weight_content),
            html.Div(id=ids.WEIGHTS_CONTAINER_TEXT)
        ]
    )
