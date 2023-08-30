import plotly.graph_objs as go
import dash_bootstrap_components as dbc

from dash import (
    dcc,
    html,
)

from builder import charactersDB

chars = charactersDB.get_names()

char_selector_dropdowns_1 = [
    dcc.Dropdown(
        options=chars,
        placeholder="Select Character",
        id={"type": "char-dropdown-sim", "index": i},
        className="dash-bootstrap",
    )
    for i in range(4)
]

char_selector_dropdowns_2 = [
    dcc.Dropdown(
        options=chars,
        placeholder="Select Character",
        id={"type": "char-dropdown-config", "index": i},
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
        ], id={"type": "char-actions", "char": i}
    )
    for i in range(4)
]


char_card_config = [
    dbc.Card(
        [
            # Config Cards
            dbc.CardBody(
                [
                    # dcc.Store(
                    #     id={"type": "char-store", "index": i},
                    #     data={"name": "", "state": True},
                    # ),
                    dbc.Row(
                        char_selector_dropdowns_1[i],
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
                                                id={
                                                    "type": "char-speed-config",
                                                    "index": i,
                                                },
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
                            dbc.Col(html.P("Energy")),
                            dbc.Col(
                                html.P(
                                    "", id={"type": "char-energy-config", "index": i}
                                )
                            ),
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(html.P("Actions")),
                        ]
                    ),
                    dbc.InputGroup(
                        [dbc.InputGroupText("Actions"), dbc.Input(
                            placeholder="Basic Basic Skill", 
                            id={"type": "char-actions-text", "index": i},
                            debounce=True,
                            pattern=r'((?:basic|skill)\s?)+'
                            )],
                        className="mb-3",
                    ),
                    dbc.InputGroup(
                        [dbc.InputGroupText("Targets"), dbc.Input(
                            placeholder="Bronya Serval Bronya", 
                            id={"type": "char-targets-text", "index": i},
                            debounce=True)],
                        className="mb-3",
                    ),
                    # char_actions[i],
                    # dbc.Button("Add", id={"type": "update-actions", "char": i}),
                ],
            ),
        ],
        class_name="col-sm-2 mt-1",
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
                        char_selector_dropdowns_2[i],
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
                                            ),
                                        ],
                                    ),
                                ],
                                className="col-sm-2",
                                style={"width": "50%", "justify-content": "center"},
                            ),
                        ]
                    ),
                    # dbc.Row(
                    #     [
                    #         dbc.Col(html.P("Sequence")),
                    #         dbc.Col(
                    #             [
                    #                 dcc.Dropdown(
                    #                     ["Basic", "Skill"],
                    #                     multi=True,
                    #                     className="dash-bootstrap",
                    #                 )
                    #             ]
                    #         ),
                    #     ]
                    # ),
                    # dbc.Row(
                    #     [
                    #         dbc.Col(html.P("Skill Target")),
                    #         dbc.Col(
                    #             [
                    #                 dcc.Dropdown(
                    #                     ["Basic", "Skill"],
                    #                     multi=True,
                    #                     className="dash-bootstrap",
                    #                 )
                    #             ]
                    #         ),
                    #     ]
                    # ),
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
            char_card_sim,
            class_name="col-sm-12",
            style={
                "display": "flex",
                "justify-content": "center",
            },
        ),
        html.Hr(),
        dbc.Row(
            children=[
                dbc.Card(
                    dbc.CardBody(
                        className="col-sm-12",
                        children=[
                            dcc.Graph(
                                id="graph",
                                figure={
                                    "layout": go.Layout(
                                        title="Plot Title",
                                        xaxis_title="Cycles",
                                        yaxis_title="Action Gauge",
                                        legend_title="Characters",
                                    )
                                },
                            ),
                        ],
                    )
                )
            ],
            style={"display": "flex"},
        ),
    ],
    # style={
    #     "display": "flex",
    #     "justify-content": "center",
    # },
)


tab_speed = html.Div()

tabs_bar = dbc.Tabs(
    [
        dbc.Tab(tab_sim_layout, label="Simulation", id="sim-tab"),
        dbc.Tab(tab_speed, label="Speed", id="speed-tab"),
        dbc.Tab(tab_config_layout, label="Config", id="config-tab"),
    ],
    id="nav-tabs",
    style={"display": "flex-inline", "justify-content": "center"},
)

page = html.Div(
    [
        tabs_bar,
        dcc.Store(
            id="legend_state", data=[{"name": "", "state": "True"} for x in range(4)]
        ),
        *[dcc.Store(id={"type": "dropdown-sync", "index": i}) for i in range(4)],
        dcc.Store(id="config-changes", data=0),
        *[dcc.Store(id={"type": "char-change", "index": i}, data=0) for i in range(4)],
    ],
)