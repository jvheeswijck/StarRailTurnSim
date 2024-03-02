import plotly.graph_objs as go
import dash_bootstrap_components as dbc

from dash import (
    dcc,
    html,
)

from .tab_config import char_card_config
from .tab_speed import tab_speed

char_selector_dropdowns = [
    dcc.Dropdown(
        options=['Loading...'],
        placeholder="Select Character",
        id={"type": "char-dropdown-sim", "index": i},
        className="dash-bootstrap",
    )
    for i in range(4)
]

char_actions = [
    dbc.Row(
        [
            dbc.Col(
                [
                    html.P("Action"),
                    dcc.Dropdown(
                        options=["Basic", "Skill"],
                        id={"type": "action-dropdown-values", "index": 0, "char": i},
                        className="dash-bootstrap",
                    ),
                ],
                id={"type": "action-dropdown-col", "char": i},
            ),
            dbc.Col(
                [
                    html.P("Target"),
                    dcc.Dropdown(
                        options=["Blank"],
                        id={"type": "action-target", "char": i, "index": 0},
                        className="dash-bootstrap",
                    ),
                ],
                id={"type": "action-target-col", "char": i},
            ),
        ],
        id={"type": "char-actions", "char": i},
    )
    for i in range(4)
]


char_card_sim = [
    dbc.Card(
        [
            dbc.CardBody(
                [
                    dcc.Store(
                        id={"type": "char-store", "index": i},
                        data={"name": "", "state": True},
                    ),
                    dbc.Row(
                        char_selector_dropdowns[i],
                        style={"width": "100%", "align-items": "center"},
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.P(
                                        "Speed",
                                        style={
                                            "align-items": "center",
                                        },
                                    )
                                ],
                                style={
                                    "width": "50%",
                                    "justify-content": "center",
                                },
                            ),
                            dbc.Col(
                                [
                                    dbc.InputGroup(
                                        [
                                            # dbc.InputGroupText("Speed"),
                                            dbc.Input(
                                                placeholder="Amount",
                                                type="number",
                                                id={"type": "char-speed", "index": i},
                                                debounce=False
                                            ),
                                        ],
                                    ),
                                ],
                                className="col-sm-2",
                                style={"width": "50%", "justify-content": "center"},
                            ),
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(html.P("Turns")),
                            dbc.Col(html.P("", id={"type": "char-turns", "index": i})),
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(html.P("Base AV")),
                            dbc.Col(
                                html.P("", id={"type": "char-av-base", "index": i})
                            ),
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(html.P("Avg AV")),
                            dbc.Col(html.P("", id={"type": "char-av-avg", "index": i})),
                        ]
                    ),
                ],
            ),
        ],
        class_name="col-sm-2 mt-1",
    )
    for i in range(4)
]

# Graph options card
graph_options_card = dbc.Card(
    dbc.CardBody(
        children=[
            dbc.Row(
                [html.H4("Options")],
                style={
                    "justify-content": "center",
                },
            ),
            dbc.Row(
                [
                    dbc.Col([html.P("AV/Cycles")]),
                    dbc.Col(
                        [
                            dbc.Switch(
                                id="av-cycles-switch",
                                label="",
                                value=False,
                            )
                        ],
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col([html.P("AV/Action Gauge")]),
                    dbc.Col(
                        [
                            dbc.Switch(
                                id="av-gauge-switch",
                                label="",
                                value=False,
                            )
                        ],
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col([html.P("Seperate Plots")]),
                    dbc.Col(
                        [
                            dbc.Switch(
                                id="use-subplots",
                                label="",
                                value=False,
                            )
                        ],
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col([html.P("Time Span")]),
                    dbc.Col(
                        [
                            dbc.Input(
                                value="450",
                                placeholder="Cycles/AV",
                                type="number",
                                min=0,
                                id="sim-duration",
                            )
                        ],
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(html.P("Start SP")),
                    dbc.Col(
                        dbc.Input(
                            value="3",
                            placeholder="3",
                            type="number",
                            id="start-sp",
                        )
                    ),
                ]
            ),
        ],
    ),
    class_name="col-sm-2 mt-1",
)

place_holder_card = dbc.Card(
    dbc.CardBody(

    ),
    class_name="col-sm-2 mt-1",
)


# Create the layout

tab_config_layout = html.Div(
    children=[
        dbc.Row(
            char_card_config,
            class_name="col-sm-12",
            style={
                "display": "flex",
                "justify-content": "center",
            },
        ),
    ]
)


tab_sim_layout = html.Div(
    children=[
        # Top row with four boxes
        dbc.Row(
            [graph_options_card] + char_card_sim + [place_holder_card],
            class_name="",
            style={
                "display": "flex",
                "justify-content": "center",
            },
            className="col-sm-12",
        ),
        html.Hr(),
        dbc.Row(
            children=[
                dbc.Card(
                    dbc.CardBody(
                        # className="col-sm-12",
                        children=[
                            dcc.Graph(
                                id="graph",
                                figure={
                                    "layout": go.Layout(
                                        xaxis_title="Cycles",
                                        yaxis_title="Character AV",
                                        legend_title="Characters",
                                        xaxis_range=(0,450),
                                        yaxis_range=(0,100),
                                        margin={'t':25},
                                    )
                                },
                            ),
                        ],
                    )
                )
            ],
            className="col-sm-12",
        ),
    ],
)


tabs_bar = dbc.Tabs(
    [
        dbc.Tab(tab_sim_layout, label="Simulation", id="sim-tab"),
        dbc.Tab(tab_speed, label="Speed", id="speed-tab"),
        dbc.Tab(tab_config_layout, label="Config", id="config-tab"),
    ],
    id="nav-tabs",
    style={"display": "flex-inline", "justify-content": "center"},
)


onload_timer = dcc.Interval(
                id='load-event',
                interval=0, # in milliseconds
                n_intervals=0,
                max_intervals=1,
            )

page = html.Div(
    [   
        onload_timer,
        tabs_bar,
        dcc.Store(
            id="legend_state", data=[{"name": "", "state": "True"} for x in range(4)]
        ),
        *[dcc.Store(id={"type": "dropdown-sync", "index": i}) for i in range(4)],
        dcc.Store(id="config-changes", data=0),
        *[dcc.Store(id={"type": "char-change", "index": i}, data=0) for i in range(4)],
    ],
)
