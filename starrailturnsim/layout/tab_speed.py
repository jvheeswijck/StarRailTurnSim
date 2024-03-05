import plotly.graph_objs as go

from dash import html, dcc
import dash_bootstrap_components as dbc

tab_speed = html.Div(
    children=[
        # Top Card Selector
        dbc.Row(
            [
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H6('Simulate Character'),
                            dcc.Dropdown(
                                options=[],
                                placeholder="Select Character",
                                id="char-dropdown-compare",
                                className="dash-bootstrap",
                            ),
                            html.H6('View Character'),
                            dcc.Dropdown(
                                options=[],
                                placeholder="Select Character",
                                id="char-dropdown-compare-view",
                                className="dash-bootstrap",
                            ),
                            # dbc.Row(
                            #     [
                            #         dbc.Col(html.P("Speed")),
                            #         dbc.Col(
                            #             [
                            #                 dbc.InputGroup(
                            #                     [
                            #                         dbc.Input(
                            #                             placeholder="Amount",
                            #                             type="number",
                            #                             id="speed-compare-input",
                            #                         )
                            #                     ]
                            #                 )
                            #             ],
                            #             className="col-sm-2",
                            #             style={
                            #                 "width": "50%",
                            #                 "justify-content": "center",
                            #             },
                            #         ),
                            #     ]
                            # ),
                        ]
                    ),
                    class_name="col-sm-3",
                ),
                dbc.Card(dbc.CardBody(dbc.Row())),
            ],
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
                                id="speed-graph",
                                figure={
                                    "layout": go.Layout(
                                        title="Speeed vs Turns",
                                        xaxis_title="Speed",
                                        yaxis_title="Turns",
                                        legend_title="Character",
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
)
