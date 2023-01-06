from dash import dcc, html
import plotly.express as px

from ..data import ids
from ..data.generate import DataSchema
from ..data.source import DataSource


def render(source: DataSource) -> html.Div:
    colours = {ids.LABEL_ONE: ids.POSITIVE_COLOUR, ids.LABEL_TWO: ids.NEGATIVE_COLOUR}
    filtered_data = source.filter(x=source.all_x, y=source.all_y, labels=source.all_labels)

    scatter = px.scatter(filtered_data.data, x=DataSchema.X_AXIS, y=DataSchema.Y_AXIS, color=DataSchema.LABELS,
                         color_discrete_map=colours, template='none')
    scatter.update_layout(
        plot_bgcolor=ids.BG_COLOUR,
        paper_bgcolor=ids.BG_COLOUR,
        legend=dict(bgcolor=ids.BG_COLOUR, title=None, orientation="h", y=1, x=0.5, yanchor='bottom', xanchor='center'),
        font_color='white'
    )
    scatter.update_traces(marker_size=10)

    return html.Div(dcc.Graph(figure=scatter, config={'staticPlot': True}), id=ids.SCATTER_PLOT)
