import traceback

from dataclasses import dataclass

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
app.layout = page

sim = Sim()
active_chars = []
config_updated = False

@dataclass
class GraphState:
    x_units : str
    y_units : str
    time_frame : int
    selected_characters : set
    need_resim : bool = False

# Sync Cards of Different Tabs
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
        return c, s
    except Exception as e:
        raise PreventUpdate
    
# @app.callback(
#     Output("char-dropdown-compare", 'options'),
#     Input({"type": "char-dropdown-sim", "index": ALL}, "value"),
# )
# def sync_compare_selection(chars : list[str]):
#     return chars

# Maintain Which Characters are Shown on Graph
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

# Update Simulation when character or speed is changed
@app.callback(
    Output({"type": "char-change", "index": MATCH}, "data"),
    Input({"type": "char-dropdown-sim", "index": MATCH}, "value"),
    Input({"type": "char-speed", "index": MATCH}, "value"),
    State({"type": "char-dropdown-sim", "index": ALL}, "value"),
    State({"type": "char-change", "index": MATCH}, "data"),
    State('sim-duration', 'value')
)
def update_turn_info(char_name : str, char_speed, char_names, change_counter, duration : int):
    
    
    # TODO: Rewrite to update on char_name None
    try:
        c = charactersDB.get(*char_names)
        print("Current chars", char_names, '|', 'Changed char:', char_name)

        if char_name is not None:
            char = charactersDB(char_name)
            trig_id = ctx.triggered_id
            print("Current id is", ctx.triggered_id )
            # if trig_id.get('type') == 'char-speed':
            try:
                charactersDB(char_name).setSpeed(char_speed)
                global sim
                sim.set_chars(c)
                sim.sort(char_names)
                sim.reset()
                sim.run()
                if change_counter is None:
                    return 1
                else:
                    return change_counter+1
            except Exception as e:
                print("Preventing update", e)
                # traceback.print_exc()
                # raise PreventUpdate
                return no_update
    except Exception as e:
        print(e)
        traceback.print_exc()
        raise PreventUpdate

# Update card information values
for i in range(4):
    @app.callback(
    Output({"type": "char-turns", "index": i}, "children"),
    Output({"type": "char-av-base", "index": i}, "children"),
    Output({"type": "char-av-avg", "index": i}, "children"),
    Input({"type": "char-change", "index": ALL}, "data"),
    State({"type": "char-dropdown-sim", "index": i}, "value")
    )
    def update_char_card(_, char_name):
        try:
            char = charactersDB(char_name)
            return char.turnCount, char.baseAV, char.avgAV
        except Exception as e:
            print("error updating character card")
            traceback.print_exc()
            raise PreventUpdate

@app.callback(
    Output("sim-duration", 'value'),
    Output("sim-duration", 'max'),
    Input('av-cycles-switch', 'value'),
    State("sim-duration", 'value')
)
def options_change(av_toggle, duration):
    duration = int(duration)
    if ctx.triggered_id == 'av-cycles-switch':
        if av_toggle:
            duration_out = int(duration / 75)
        else:
            duration_out = int(duration) * 75
    else:
        duration_out = no_update
        
    max_value = 20 if av_toggle else 1575

    return duration_out, max_value
    
                    

# Update Graph
@app.callback(
    Output("graph", "figure"),
    Input("nav-tabs", "active_tab"),
    Input({"type": "char-change", "index": ALL}, "data"),
    Input("sim-duration", 'value'),
    Input('start-sp', 'value'),
    Input("av-gauge-switch", 'value'),
    State({"type": "char-dropdown-sim", "index": ALL}, "value"),
    State("legend_state", "data"),
    State('av-cycles-switch', 'value'),
)
def update_graph(active_tab, 
                 _, 
                 duration, 
                 start_sp,
                 gauge_toggle,
                 char_names, 
                 char_state,
                 av_toggle):
    print("Attempting to update graph")
    # y_target = 'AV Value'
    # y_target = ''
    
    # Add logic to prevent simlatuions when unnecessary
    
    try:
        global config_updated
        if active_tab == "tab-2":
            raise PreventUpdate
        
        timeframe = int(duration)
        if ctx.triggered_id == 'sim-duration':
            if av_toggle:
                timeframe = int(duration) * 75
            else:
                timeframe = int(duration)
            if sim.timeFrame < timeframe:
                config_updated = True
            
        if config_updated:
            sim.set_chars(charactersDB.get(*char_names))
            sim.set_sp(start_sp)
            sim.reset()
            sim.run(timeframe)
            config_updated = False

        df = sim.build_dataframe()

        choice = "Cycles" if av_toggle else "AV"
        x_max = duration
        if gauge_toggle:
            y_val = "AV Value"
        else:
            y_val = "Action Gauge"
        

        if choice == "Cycles":
            fig = df.plot.line(
                x="Cycles", y=y_val, color="Character", hover_data=["Turns"]
            )
            x_max = duration
            fig.update_xaxes(range=[0, x_max])
            fig.update_layout(xaxis={"dtick": 1})

        else:
            x_max = duration
            fig = df.plot.line(x="Elapsed Action Value", y=y_val, color="Character")
            fig.update_xaxes(range=[0, x_max])
            fig.update_layout(xaxis={"dtick": 75})

        for e in char_state:
            if e["state"] == "legendonly":
                fig.update_traces(visible="legendonly", selector=({"name": e["name"]}))

        fig.update_layout(hovermode="x")
        
        return fig
    except Exception as e:
        print(e)
        traceback.print_exc()
        raise PreventUpdate

# Display speed when character is selected
@app.callback(
    Output({"type": "char-speed", "index": MATCH}, "value"),
    Input({"type": "char-dropdown-sim", "index": MATCH}, "value"),
)
def update_speed_info(char_name):
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
            global config_updated
            config_updated = True
        else:
            print('No update')
    except Exception as e:
        print(e)
        traceback.print_exc()
        raise PreventUpdate
    
    
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
