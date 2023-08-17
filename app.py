import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
from dash import (
    ALL,
    MATCH,
    Dash,
    Input,
    Output,
    Patch,
    State,
    callback,
    ctx,
    dcc,
    html,
    no_update,
)
from dash.exceptions import PreventUpdate

# from dash_extensions import Monitor

from builder import CharacterManager
from sim import Sim

pd.options.plotting.backend = "plotly"


# Initialize the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])


charactersDB = CharacterManager()
charactersDB("Bronya").setBasicTarget(charactersDB("Bronya"))
charactersDB("Bronya").setSkillTarget(charactersDB("Sushang"))
charactersDB("Bronya").setActionSeq(["basic", "skill"])
chars = charactersDB.get_names()
sim = Sim()
config_updated = False

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

# @app.callback(
#     Output({"type": "char-actions", "char": MATCH}, 'children'),
#     Input({"type": "update-actions", "char": MATCH}, 'n_clicks'),
# )
# def add_new_action_line(_):
#     i = ctx.triggered_id['char']
#     l = Patch()
#     l.append(
#         dbc.Col(
#                 [
#                     html.P("Action"),
#                     dcc.Dropdown(
#                         options=["Basic", "Skill"],
#                         id={"type": "action-dropdown-values", "index": , "char": i},
#                         className="dash-bootstrap",
#                     ),
#                 ],
#                 id={"type": "action-dropdown-col", "char": i},
#             ),
#             dbc.Col(
#                 [
#                     html.P("Target"),
#                     dcc.Dropdown(
#                         options=["Blank"],
#                         id={"type": "action-target", "char": i, "index": },
#                         className="dash-bootstrap",
#                     ),
#                 ],
#                 id={"type": "action-target-col", "char": i},
#             ),
#     )

    
#     raise PreventUpdate
#     l = Patch()
#     l.append(
#         dbc.Col(
#                 [
#                     html.P("Action"),
#                     dcc.Dropdown(
#                         options=["Basic", "Skill"],
#                         id={"type": "action-dropdown-values", "index": 0, "char": i},
#                         className="dash-bootstrap",
#                     ),
#                 ],
#                 id={"type": "action-dropdown-col", "char": i},
#             ),
#             dbc.Col(
#                 [
#                     html.P("Target"),
#                     dcc.Dropdown(
#                         options=["Blank"],
#                         id={"type": "action-target", "char": i, "index": 0},
#                         className="dash-bootstrap",
#                     ),
#                 ],
#                 id={"type": "action-target-col", "char": i},
#             ),
#     )



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

app.layout = html.Div(
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


######################################################################################


# Not working?

# for i in range(4):

#     @app.callback(
#         Output({"type": "action-dropdown-col", "index": i}, "children"),
#         Input({"type": "action-dropdown-values", "index": ALL, "char": i}, "value"),
#     )
#     def new_action(val):
#         print("ctx id", ctx.triggered_id)
#         print("children length", len(val))
#         print("the children are", val)
#         patcher = Patch()
#         new_drop = dcc.Dropdown(
#             options=["Basic", "SKill"],
#             id={"type": "action-dropdown-values", "index": len(val)},
#             className="dash-bootstrap",
#         )

#         patcher.append(new_drop)
#         return patcher


# @app.callback(
#     Output({"type": "action-dropdown-col", "char": MATCH}, "children"),
#     Input({"type": "action-dropdown-values", "char": MATCH, "index": ALL}, "value"),
#     State({"type": "action-dropdown-col", "char": MATCH}, "children"),
# )
# def new_action(val, childs):
#     print("ctx id", ctx.triggered_id)
#     print("children length", len(childs))
#     print("the children are", val)

#     try:
#         trigger_id = ctx.triggered_id["index"]
#         if trigger_id == len(childs) - 1:
#             patcher = Patch()
#             new_drop = dcc.Dropdown(
#                 options=["Basic", "Skill"],
#                 id={"type": "action-dropdown-values", "index": len(childs)},
#                 className="dash-bootstrap",
#             )
#             patcher.append(new_drop)
#             return patcher
#     except Exception as e:
#         print(e)
#         raise PreventUpdate
# @app.callback(
#     Output({"type": "action-dropdown-col", "char": }, "children"),
#     Input({"type": "action-dropdown-values", "char": MATCH, "index": ALL}, "value"),
# )


# Rework this
# @app.callback(
#     Output({"type": "action-dropdown-col", "char": 0}, "children"),
#     Input({"type": "action-dropdown-values", "index": 0, "char": 0}, "value"),
#     State({"type": "action-dropdown-values", "index": ALL, "char": 0}, "value"),
# )
# def test(val, vals):
#     print("All vals are", vals)
#     index = ctx.triggered_id["index"]
#     if index == len(vals) - 1:
#         patcher = Patch()
#         new_drop = dcc.Dropdown(
#             options=["Basic", "Skill"],
#             id={"type": "action-dropdown-values", "index": len(vals), "char": 0},
#             className="dash-bootstrap",
#         )

#         @app.callback(
#             Output({"type": "action-dropdown-col", "char": 0}, "children"),
#             Input(
#                 {"type": "action-dropdown-values", "index": len(vals), "char": 0},
#                 "value",
#             ),
#             State({"type": "action-dropdown-values", "index": ALL, "char": 0}, "value"),
#         )
#         def new_box(val, vals):
#             if index == len(vals) - 1:
#                 patcher = Patch()
#                 new_drop = dcc.Dropdown(
#                     options=["Basic", "Skill"],
#                     id={"type": "action-dropdown-values", "index": len(vals)},
#                     className="dash-bootstrap",
#                 )
#                 patcher.append(new_drop)
#                 return patcher
#             else:
#                 return no_update

#         patcher.append(new_drop)
#         return patcher
#     else:
#         return no_update


@app.callback(
    Output({"type": "char-dropdown-config", "index": MATCH}, "value"),
    Output({"type": "char-dropdown-sim", "index": MATCH}, "value"),
    Input({"type": "char-dropdown-config", "index": MATCH}, "value"),
    Input({"type": "char-dropdown-sim", "index": MATCH}, "value"),
)
def sync_dropdown(config, sim):
    try:
        c = no_update if ctx.triggered_id["type"] == "char-dropdown-config" else sim
        s = no_update if ctx.triggered_id["type"] == "char-dropdown-sim" else config
    except Exception as e:
        raise PreventUpdate

    return c, s





# Update when characters change or graph is restyled
@app.callback(
    Output("legend_state", "data"),
    Input({"type": "char-dropdown-sim", "index": ALL}, "value"),
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


@app.callback(
    Output({"type": "char-turns", "index": MATCH}, "children"),
    Output({"type": "char-av-base", "index": MATCH}, "children"),
    Output({"type": "char-av-avg", "index": MATCH}, "children"),
    Output({"type": "char-change", "index": MATCH}, "data"),
    Input({"type": "char-dropdown-sim", "index": MATCH}, "value"),
    Input({"type": "char-speed", "index": MATCH}, "value"),
    State({"type": "char-dropdown-sim", "index": ALL}, "value"),
    State({"type": "char-change", "index": MATCH}, "data")
)
def update_turn_info(char_name : str, char_speed, char_names, data):
    try:
        c = charactersDB.get(*char_names)
        if char_name is not None:
            char = charactersDB(char_name)
            trig_id = ctx.triggered_id
            if trig_id.get('type') == 'char-speed':
                try:
                    charactersDB(char_name).setSpeed(char_speed)
                except Exception:
                    pass
            
            
        sim.set_chars(c)
        sim.reset()
        sim.run(750)
        
        if char_name is None:
            return 0,0,0,data+1
        else:
            return char.turnCount, char.baseAV, char.avgAV, data+1
    except Exception as e:
        print(e)
        return no_update, no_update, no_update, no_update


# Update Graph
@app.callback(
    Output("graph", "figure"),
    Input("nav-tabs", "active_tab"),
    Input({"type": "char-change", "index": ALL}, "data"),
    State({"type": "char-dropdown-sim", "index": ALL}, "value"),
    # Input({"type": "char-speed", "index": ALL}, "value"),
    State("legend_state", "data"),
)
def update_graph(active_tab, _, char_names, char_state):
    try:
        if active_tab == "tab-2":
            raise PreventUpdate
        global config_updated
        if config_updated:
            
            sim.set_chars(charactersDB.get(*char_names))
            sim.reset()
            sim.run(750)
            config_updated = False

        df = sim.build_dataframe()

        choice = "Cycles"
        # Unhardcode this
        x_max = 0

        if choice == "Cycles":
            fig = df.plot.line(
                x="Cycles", y="Action Gauge", color="Character", hover_data=["Turns"]
            )
            x_max = 10
            fig.update_xaxes(range=[0, x_max])
            fig.update_layout(xaxis={"dtick": 1})

            # fig.update_traces(visible='legendonly', selector = ({'name':'Bronya'}))
        else:
            x_max = 750
            fig = df.plot.line(x="Action Value", y="Action Gauge", color="Character")
            fig.update_xaxes(range=[0, x_max])
            fig.update_layout(xaxis={"dtick": 75})

        for e in char_state:
            if e["state"] == "legendonly":
                fig.update_traces(visible="legendonly", selector=({"name": e["name"]}))

        # fig.update_traces(hovertemplate='GDP: %{x} <br>Life Expectancy: %{y}')
        fig.update_layout(hovermode="x")
        
        return fig
    except Exception as e:
        return no_update


@app.callback(
    Output({"type": "char-speed", "index": MATCH}, "value"),
    Input({"type": "char-dropdown-sim", "index": MATCH}, "value"),
)
def update_card(char_name):
    try:
        return charactersDB(char_name).baseSpeed
    except KeyError:
        return 0
    
@app.callback(
    Output('config-changes', 'data'),
    Input({"type": "char-actions-text", "index": ALL}, 'value'),
    Input({"type": "char-targets-text", "index": ALL}, 'value'),
    State({'type':'char-dropdown-config', "index": ALL}, 'value')
)
def update_actions(actions, targets, char_names):
    if ctx.triggered_id is None:
        raise PreventUpdate
    print('================')
    print("Update actions is running")
    print(ctx.triggered_id)
    try:
        char_index = ctx.triggered_id['index']
        print('char index', char_index)
        char = charactersDB(char_names[char_index])
        if ctx.triggered_id['type'] == 'char-actions-text':
            s = actions[char_index]
            print('s', s)
            valid_acts = [x.lower() for x in s.split() if x.lower() in ['basic', 'skill']]
            char.setActionSeq(valid_acts)
        else:
            print('Else')
    except Exception as e:
        print(e)
    
    
    return no_update

@app.callback(
    Output({"type": "char-actions-text", "index": MATCH}, 'pattern'),
    Input({"type": "char-actions-text", "index": MATCH}, 'value'),
    State({'type':'char-dropdown-config', "index": MATCH}, 'value')
)
def update_actions_css(actions, char_names):
    return '(basic)|(skill)'

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)


# Configure page where you can set the character parameters, and action sequence, and targets
# Third page is turns vs speed
# Add settings to toggle between action value and cycles
# Fix discrepency between base AV and avg AV
