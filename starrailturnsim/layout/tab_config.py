import dash_bootstrap_components as dbc
from dash import (
    dcc,
    html,
)

char_selector_dropdowns = [
    dcc.Dropdown(
        options=[],
        placeholder="Select Character",
        id={"type": "char-dropdown-config", "index": i},
        className="dash-bootstrap",
    )
    for i in range(4)
]

char_card_config = [
    dbc.Card(
        [
            # Config Cards
            dbc.CardBody(
                [
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
                        [
                            dbc.InputGroupText("Actions"),
                            dbc.Input(
                                placeholder="Basic Basic Skill",
                                id={"type": "char-actions-text", "index": i},
                                debounce=True,
                                pattern=r"((?:basic|skill)\s?)+",
                            ),
                        ],
                        className="mb-3",
                    ),
                    dbc.InputGroup(
                        [
                            dbc.InputGroupText("Targets"),
                            dbc.Input(
                                placeholder="Bronya Serval Bronya",
                                id={"type": "char-targets-text", "index": i},
                                debounce=True,
                            ),
                        ],
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