from dataclasses import dataclass
import itertools

from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from app.data import ids


@dataclass
class WeightSlider:
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


def render(app: Dash, input_count: int) -> html.Div:

    @app.callback(
        Output(ids.WEIGHTS_CONTAINER, "children"),
        Input(ids.WEIGHT_SLIDER, "value")
    )
    def update_output(value: int) -> str:
        return f'You have selected {value}'

    indices = [i for i in range(1, input_count+1)] * input_count
    indices.sort()

    slider_titles = [html.H6(f'w{i}_{idx}') for _, group in itertools.groupby(indices) for idx, i in enumerate(group, start=1)]
    sliders = [WeightSlider(id=f'{i}').create() for i in range(len(slider_titles))]
    weight_content = list(itertools.chain.from_iterable(zip(slider_titles, sliders)))

    return html.Div(
        id=ids.WEIGHTS_CONTAINER,
        className=['mt-5'],
        children=[
            html.H5('Weights'),
            html.Div(id=ids.WEIGHT_SLIDER_CONTAINER, children=weight_content),
        ]
    )
