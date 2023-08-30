import dash_bootstrap_components as dbc
import pandas as pd
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
    no_update,
)
from dash.exceptions import PreventUpdate

from layout import page

from builder import charactersDB
from sim import Sim

pd.options.plotting.backend = "plotly"

# Initialize the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])

sim = Sim()
config_updated = False

app.layout = page


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

# Seperate callback for each card

# for i in range(4):
#     def update_char_card():
#         pass


# # Need call


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
