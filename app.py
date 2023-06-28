from itertools import chain

import dash_bootstrap_components as dbc

import pandas as pd
from dash import Dash, dcc, html, Input, Output, State, callback, ctx, MATCH, ALL
import plotly.graph_objs as go

import plotly.express as px

from sim import Sim
from builder import CharacterManager

pd.options.plotting.backend = "plotly"


# Initialize the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])


charactersDB = CharacterManager()
charactersDB("Bronya").setSkillTarget(charactersDB("Sushang"))
charactersDB("Bronya").setActionSeq(["basic", "skill"])
chars = charactersDB.get_names()

# nav = dbc.Nav(
#     [
#         dbc.NavItem(dbc.NavLink("Characters", active=True, n_clicks=0)),
#         dbc.NavItem(dbc.NavLink("Simulation", n_clicks=0)),
#         dbc.NavItem(dbc.NavLink("Speed", n_clicks=0)),
#     ],

# )

# tab1_content = dbc.Card(
#     dbc.CardBody(
#         [
#             html.P("This is tab 1!", className="card-text"),
#             dbc.Button("Click here", color="success"),
#         ]
#     ),
#     className="mt-3",
# )

# tab2_content = dbc.Card(
#     dbc.CardBody(
#         [
#             html.P("This is tab 2!", className="card-text"),
#             dbc.Button("Don't click here", color="danger"),
#         ]
#     ),
#     className="mt-3",
# )


char_selector_dropdowns = [
    dcc.Dropdown(
        options=chars,
        placeholder="Select Character",
        id={"type": "char-dropdown", "index": i},
        className="dash-bootstrap",
    )
    for i in range(4)
]


character_cards = [
    dbc.Card(
        [
            dbc.CardBody(
                [
                    dbc.Row(
                        char_selector_dropdowns[i],
                        style={"width": "100%", "align-items": "center"},
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                [html.P("Speed", style={"align-items": "center",})],
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
                ],
            ),
        ],
        class_name="col-sm-2 mt-1",
        # style={"flex-grow": "4"},
        # style={
        #     "max-width": "25%",
        #     "min-widt": "23%",
        #     "left-margin": "0.25rem",
        #     "right-margin": "0.25rem",
        # },
    )
    for i in range(4)
]


# Create the layout


tab_simulation = html.Div(
    children=[
        # Top row with four boxes
        dbc.Row(
            character_cards,
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
                            dcc.Graph(id="graph"),
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

tab_characters = dbc.Card(
    dbc.CardBody(
        [
            html.P("This is tab 1!", className="card-text"),
            dbc.Button("Click here", color="success"),
        ]
    ),
    className="col-sm-12 mt-4",
)
tab_speed = html.Div()


tabs = dbc.Tabs(
    [
        dbc.Tab(tab_simulation, label="Simulation"),
        dbc.Tab(tab_speed, label="Speed"),
        dbc.Tab(tab_characters, label="Characters"),
        # dbc.Tab(
        #     "This tab's content is never seen", label="Tab 3", disabled=True
        # ),
    ],
    style={"display": "flex-inline", "justify-content": "center"},
)

app.layout = html.Div(tabs)


# Update Graph
@app.callback(
    Output("graph", "figure"),
    Input({"type": "char-dropdown", "index": ALL}, "value"),
    Input({"type": "char-speed", "index": ALL}, "value"),
)
def character_change(char_name, char_speed):
    for name, speed in zip(char_name, char_speed):
        try:
            charactersDB(name).setSpeed(speed)
        except Exception:
            continue
    return update_line_chart(*char_name)


def update_line_chart(n1, n2, n3, n4):
    c = charactersDB.get(n1, n2, n3, n4)
    sim = Sim(c)
    sim.reset()
    sim.run(750)

    data = list(
        chain(
            *[
                [(i, name, x) for i, x in enumerate(char.history)]
                for name, char in sim.characters.items()
            ]
        )
    )

    # Add turns to hover
    df = pd.DataFrame.from_records(
        data, columns=["Action Value", "Character", "Action Gauge"]
    )
    fig = df.plot.line(x="Action Value", y="Action Gauge", color="Character")
    fig.update_layout(hovermode="x unified")
    fig.update_layout(xaxis={"dtick": 75})
    # fig = px.line(df, y=[n1, n2, n3, n4])
    return fig


@app.callback(
    Output({"type": "char-speed", "index": MATCH}, "value"),
    Input({"type": "char-dropdown", "index": MATCH}, "value"),
)
def update_card(char_name):
    try:
        return charactersDB(char_name).baseSpeed
    except KeyError:
        return 0


# @app.
# def update_turns(char_name):
#     return o


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)


# Configure page where you can set the character parameters, and action sequence, and targets
# Third page is turns vs speed
