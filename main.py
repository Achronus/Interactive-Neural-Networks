import os

from dash import Dash
from dash_bootstrap_components.themes import DARKLY

from app.data import ids
from app.data.generate import set_data
from app.data.source import DataSource
from app.layout import create_layout

debug = False if os.environ["DASH_DEBUG_MODE"] == "False" else True

app = Dash(__name__, external_stylesheets=[DARKLY])
server = app.server

data = set_data(n_points=50, n_positive=10, threshold=13)

app.title = ids.APP_TITLE
app.layout = create_layout(app, DataSource(data))


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=debug, threaded=True)
