from dataclasses import dataclass
import itertools

from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from app.components import scatter_plot
from app.data import ids
from app.data.source import DataSource


@dataclass
class ParameterSlider:
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
            id=self.id,
            marks={
                self.min: {'label': str(self.min)},
                self.value: {'label': str(self.value)},
                self.max: {'label': str(self.max)}
            },
            tooltip={"placement": "bottom", "always_visible": True}
        )


class AssignContent:
    """Helper class for assigning weights and biases into respective `html.Divs`."""
    def __init__(self, title_id: str, slider_id: str) -> None:
        self.title_id = title_id
        self.slider_id = slider_id

    def set_with_groupby(self, data: list[float], indices: list[int]) -> list:
        """
        Creates and merge titles and sliders into a list using `itertools.groupby`. Used for weight indexing.

        :param data: (list[float]) a list of float data
        :param indices: (list[int]) a list of duplicate indices in ascending order. For example, [1, 1, 2, 2]

        :return: a list of html.H6 and dcc.Slider objects in respective order
        """
        titles = [html.H6(f'{self.title_id}{i}_{idx}') for _, group in itertools.groupby(indices) for idx, i in enumerate(group, start=1)]
        sliders = [ParameterSlider(id=f'{self.slider_id}-{i}', value=data[i]).create() for i in range(len(titles))]
        return list(itertools.chain.from_iterable(zip(titles, sliders)))

    def set_with_range(self, data: list[float]) -> list:
        """
        Creates and merges titles and sliders into a list using a standard list comprehension. Used for bias indexing.

        :param data: (list[float]) a list of float data

        :return: a list of html.H6 and dcc.Slider objects in respective order
        """
        titles = [html.H6(f'{self.title_id}_{i+1}') for i in range(len(data))]
        sliders = [ParameterSlider(id=f'{self.slider_id}-{i}', value=data[i]).create() for i in range(len(titles))]
        return list(itertools.chain.from_iterable(zip(titles, sliders)))


def render_simple_params_no_hidden(app: Dash, data: DataSource, weights: list[float], biases: list[float]) -> html.Div:
    """
    Creates weight slider data for a neural network containing two inputs and two outputs (no hidden layers) and
    uses a callback to update its corresponding scatter plot when sliders are changed.

    :param app: (Dash) an existing Dash application
    :param data: (DataSource) a data source object containing data
    :param weights: (list[float]) a predefined set of weights
    :param biases: (list[float]) a predefined set of biases

    :return: a dash html.Div containing weight sliders
    """
    input_count = 2
    indices = [i for i in range(1, input_count+1)] * input_count
    indices.sort()  # [1, 1, 2, 2]

    weight_content = AssignContent(title_id='w', slider_id=ids.WEIGHT_SLIDER).set_with_groupby(weights, indices=indices)
    bias_content = AssignContent(title_id='b', slider_id=ids.BIAS_SLIDER).set_with_range(biases)

    @app.callback(
        Output(ids.SCATTER_PLOT1_CONTAINER, "children"),
        [
            Input(f'{ids.WEIGHT_SLIDER}-0', "value"),
            Input(f'{ids.WEIGHT_SLIDER}-1', "value"),
            Input(f'{ids.WEIGHT_SLIDER}-2', "value"),
            Input(f'{ids.WEIGHT_SLIDER}-3', "value"),
            Input(f'{ids.BIAS_SLIDER}-0', "value"),
            Input(f'{ids.BIAS_SLIDER}-1', "value")
        ]
    )
    def update_plot(w1: float, w2: float, w3: float, w4: float, b1: float, b2: float) -> html.Div:
        return scatter_plot.render_no_hidden(data, weights=[w1, w2, w3, w4], biases=[b1, b2])

    return html.Div(
        id=ids.SLIDER_CONTAINER,
        className=['mt-5'],
        children=[
            html.Div(
                id=ids.WEIGHT_CONTAINER,
                className=['mb-3'],
                children=[
                    html.H5('Weights'),
                    html.Div(id=ids.WEIGHT_SLIDER_CONTAINER, children=weight_content)
                ]
            ),
            html.Div(
                id=ids.BIAS_CONTAINER,
                className=['mt-3'],
                children=[
                    html.H5('Biases'),
                    html.Div(id=ids.BIAS_SLIDER_CONTAINER, children=bias_content)
                ]
            )
        ]
    )
