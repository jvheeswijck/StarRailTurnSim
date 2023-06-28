import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
from dash import ALL, MATCH, Dash, Input, Output, Patch, State, callback, ctx, dcc, html

from builder import CharacterManager
from sim import Sim

pd.options.plotting.backend = "plotly"


# Initialize the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])


charactersDB = CharacterManager()
charactersDB("Bronya").setSkillTarget(charactersDB("Sushang"))
charactersDB("Bronya").setActionSeq(["skill", "skill"])
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

app.layout = html.Div(
    [
        tabs,
        dcc.Store(
            id="legend_state", data=[{"name": "", "state": "True"} for x in range(4)]
        ),
    ],
)

######################################################################################


# Update when characters change or graph is restyled
@app.callback(
    Output("legend_state", "data"),
    Input({"type": "char-dropdown", "index": ALL}, "value"),
    Input("graph", "restyleData"),
    State("legend_state", "data"),
)
def update_char_state(characters, graph_style, legend_state):
    # Update character names
    for i, v in enumerate(legend_state):
        v["name"] = characters[i]

    # Update legend state
    if graph_style is not None:
        legend_state[graph_style[1][0]]["state"] = graph_style[0]["visible"][0]

    return legend_state


# Update Graph
@app.callback(
    Output("graph", "figure"),
    Input({"type": "char-dropdown", "index": ALL}, "value"),
    Input({"type": "char-speed", "index": ALL}, "value"),
    # State({"type": "char-store", "index": ALL}, "data"),
    State("legend_state", "data"),
)
def character_change(char_name, char_speed, char_state):
    for name, speed in zip(char_name, char_speed):
        try:
            charactersDB(name).setSpeed(speed)
        except Exception:
            continue

    c = charactersDB.get(*char_name)

    sim = Sim(c)
    sim.reset()
    sim.run(750)
    df = sim.build_dataframe()

    choice = "Cycles"
    if choice == "Cycles":
        fig = df.plot.line(
            x="Cycles", y="Action Gauge", color="Character", hover_data=["Turns"]
        )
        fig.update_layout(xaxis={"dtick": 1})

        # fig.update_traces(visible='legendonly', selector = ({'name':'Bronya'}))
    else:
        fig = df.plot.line(x="Action Value", y="Action Gauge", color="Character")
        fig.update_layout(xaxis={"dtick": 75})

    for e in char_state:
        if e["state"] == "legendonly":
            fig.update_traces(visible="legendonly", selector=({"name": e["name"]}))

    # fig.update_traces(hovertemplate='GDP: %{x} <br>Life Expectancy: %{y}')
    fig.update_layout(hovermode="x unified")
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


@app.callback(
    Output({"type": "char-turns", "index": MATCH}, "children"),
    Input({"type": "char-dropdown", "index": MATCH}, "value"),
    Input({"type": "char-speed", "index": MATCH}, "value"),
)
def update_turns(char_name, char_speed):
    try:
        c = charactersDB(char_name)
        perc = (c.actionGauge / c.currentSpeed) / 75
        return c.turnCount + round(perc, 2)
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
# Add settings to toggle between action value and cycles
