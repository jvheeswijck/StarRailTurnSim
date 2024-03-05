import traceback
import logging
import os
from dataclasses import dataclass
from pprint import pprint

import polars as pl
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from dash import (
    ALL,
    MATCH,
    Dash,
    Input,
    Output,
    State,
    ctx,
    no_update,
)

from dash.exceptions import PreventUpdate

from layout.index import page
from builder import charactersDB
from sim import Sim

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Initialize the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])
app.layout = page

sim = Sim()
charactersDB.set_BattleHandler(sim)
active_chars = []
config_updated = False
chars = charactersDB.get_names()
show_character = [True, True, True, True]
colors = ['CornflowerBlue', 'FireBrick', 'green', 'purple']


@dataclass
class GraphState:
    x_units: str
    y_units: str
    time_frame: int
    selected_characters: set
    need_resim: bool = False


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
    except Exception:
        raise PreventUpdate


# Maintain Which Characters are Shown on Graph
@app.callback(
    Output("legend_state", "data"),
    Input({"type": "char-dropdown-sim", "index": ALL}, "value"),
    Input("graph", "restyleData"),
    State("legend_state", "data"),
)
def update_char_state(characters, graph_style, legend_state):
    # Update character names
    # logging.debug("Characters are " + characters)
    # logging.debug("Graph_Style is " + graph_style)
    # logging.debug("Legend state is " + legend_state)
    # print('Graph style changing')
    # print(graph_style)

    for i, v in enumerate(legend_state):
        v["name"] = characters[i]

    # Update legend state
    if graph_style is not None:
        legend_state[graph_style[1][0]]["state"] = graph_style[0]["visible"][0]
        # print('The state of the trace is', graph_style[0]['visible'])
        show_character[graph_style[1][0]] = (
            False if (graph_style[0]["visible"][0] == "legendonly") else True
        )

    # print('The current legend status is ', show_character)
    return legend_state


# Update Simulation when character or speed is changed
# This can be refractored to remove the MATCH condition
@app.callback(
    Output({"type": "char-change", "index": MATCH}, "data"),
    Input({"type": "char-dropdown-sim", "index": MATCH}, "value"),
    Input({"type": "char-speed", "index": MATCH}, "value"),
    State({"type": "char-dropdown-sim", "index": ALL}, "value"),
    State({"type": "char-change", "index": MATCH}, "data"),
    State("sim-duration", "value"),
)
def update_turn_info(
    char_name: str, char_speed, char_names, change_counter, duration: int,
):
    # TODO: Allow updating when character is removed
    try:
        c = charactersDB.get(*char_names)

        if char_name is not None:
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
                    return change_counter + 1
            except Exception:
                # logging.error("Preventing update %s", e)
                # traceback.print_exc()
                logger.debug("Error updating sim")
                return no_update, no_update
    except Exception as e:
        logging.debug(e)
        traceback.print_exc()
        raise PreventUpdate



# Refactored element change stuff

        # Output('main-sim-update', 'data'),
#

# @app.callback(
#     Output({"type": "char-turns", "index": i}, "children"),
#     Output({"type": "char-av-base", "index": i}, "children"),
#     Output({"type": "char-av-avg", "index": i}, "children"),
#     Input({"type": "char-change", "index": ALL}, "data"),
#     State({"type": "char-dropdown-sim", "index": i}, "value"),
# )
# def update_char_card(_, char_name, sim_update):
#     try:
#         char = charactersDB(char_name)
#         return char.totalTurnCount, char.baseAV, char.avgAV, sim_update+1
#     except Exception:
#         # logging.warning("error updating character card")
#         # traceback.print_exc()
#         raise PreventUpdate


# Update card information values
for i in range(4):

    @app.callback(
        Output({"type": "char-turns", "index": i}, "children"),
        Output({"type": "char-av-base", "index": i}, "children"),
        Output({"type": "char-av-avg", "index": i}, "children"),
        Input({"type": "char-change", "index": ALL}, "data"),
        State({"type": "char-dropdown-sim", "index": i}, "value"),
    )
    def update_char_card(_, char_name):
        try:
            char = charactersDB(char_name)
            return char.totalTurnCount, char.baseAV, char.avgAV
        except Exception:
            # logging.warning("error updating character card")
            # traceback.print_exc()
            raise PreventUpdate


@app.callback(
    Output("sim-duration", "value"),
    Output("sim-duration", "max"),
    Input("av-cycles-switch", "value"),
    State("sim-duration", "value"),
)
def options_change(av_toggle, duration):
    duration = int(duration)
    if ctx.triggered_id == "av-cycles-switch":
        if av_toggle:
            duration_out = round((duration - 75) / 75, 1)
        else:
            duration_out = int(duration) * 75 + 75
    else:
        duration_out = no_update

    max_value = 20 if av_toggle else 1575

    return duration_out, max_value


# Update Graph
# TODO: move the update sim state to a separte place
@app.callback(
    Output("graph", "figure"),
    Output('main-sim-update', 'data'),
    Input("nav-tabs", "active_tab"),
    Input({"type": "char-change", "index": ALL}, "data"),
    Input("sim-duration", "value"),
    Input("start-sp", "value"),
    Input("av-gauge-switch", "value"),
    Input("use-subplots", "value"),
    State("graph", "restyleData"),
    State({"type": "char-dropdown-sim", "index": ALL}, "value"),
    State("legend_state", "data"),
    State("av-cycles-switch", "value"),
    State("graph", "figure"),
    State('main-sim-update', 'data')
)
def update_graph(
    active_tab,
    _,
    duration,
    start_sp,
    gauge_toggle,
    use_subplots,
    restyleData,
    char_names,
    char_state,
    av_toggle,
    graph_fig,
    sim_update:int
):
    # Add logic to prevent simlatuions when unnecessary
    if ctx.triggered_id == "graph":
        raise PreventUpdate

    try:
        global config_updated
        if active_tab == "tab-2":
            raise PreventUpdate

        duration = int(duration)
        timeframe = int(duration)
        if ctx.triggered_id == "sim-duration":
            if av_toggle:
                timeframe = int(duration) * 75 + 75
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

        choice = "Cycles" if av_toggle else "Elapsed Action Value"
        if gauge_toggle:
            y_val = "Action Gauge"
            y_title = "Character Action Gauge"
        else:
            y_val = "AV Value"
            y_title = "Character Action Value"

        state_dict = {
            x[0]: x[1] for x in zip(char_names, show_character) if x[0] is not None
        }

        # Build the graph lines from the Polars DataFrame
        lines: list[go.Scatter] = []
        for c in char_names:
            if c is None:
                continue
            df_c = df.filter(pl.col("Character") == c)
            isVisible = True if state_dict[c] else "legendonly"
            line_obj = go.Scatter(
                x=df_c.select(choice).to_series().to_list(),
                y=df_c.select(y_val).to_series().to_list(),
                name=c,
                legendrank=char_names.index(c),
                visible=isVisible,
            )
            lines.append(line_obj)

        num_plots = 1
        if use_subplots:
            for i, trace in enumerate(lines):
                if state_dict[trace.name] is True:
                    num_plots += 1
            if num_plots != 1:
                num_plots -= 1

        # Make Axis
        xmax = duration + 1 if av_toggle else duration
        go_fig = make_subplots(
            rows=num_plots,
            cols=1,
            shared_xaxes=True,
            x_title=choice,
            y_title=y_title,
            vertical_spacing=0.04,
        )

        go_fig.update_yaxes({"autorange": True, "fixedrange": True})
        go_fig.update_xaxes({"range": (0, xmax * 1.03)})
        go_fig.update_layout(
            margin={"t": 25, "b": 50},
        )

        if av_toggle:
            tickvals = list(range(int(xmax + 1)))
            ticktext = list(map(lambda x: str(x - 1), tickvals))
            go_fig.update_xaxes(
                {"tickmode": "array", "tickvals": tickvals, "ticktext": ticktext}
            )

        if use_subplots:
            fill_index = 0
            for i, trace in enumerate(lines):
                if state_dict[trace.name]:
                    fill_index += 1
                else:
                    if fill_index == 0:
                        fill_index = 1
                go_fig.add_trace(trace, row=fill_index, col=1)
                if i == 0 and not state_dict[trace.name]:
                    fill_index = 0

        else:
            for li in lines:
                go_fig.add_trace(li, row=1, col=1)

        return go_fig, sim_update
    except Exception as e:
        logging.warning(e)
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
    Output("config-changes", "data"),
    Input({"type": "char-actions-text", "index": ALL}, "value"),
    Input({"type": "char-targets-text", "index": ALL}, "value"),
    State({"type": "char-dropdown-config", "index": ALL}, "value"),
)
def update_actions(actions, targets, char_names):
    if ctx.triggered_id is None:
        raise PreventUpdate
    logging.debug("================Update actions is running================")
    logging.debug(str(ctx.triggered_id))
    try:
        char_index = ctx.triggered_id["index"]
        print("char index", char_index)
        char = charactersDB(char_names[char_index])
        if ctx.triggered_id["type"] == "char-actions-text":
            s = actions[char_index]
            print("s", s)
            valid_acts = [
                x.lower() for x in s.split() if x.lower() in ["basic", "skill"]
            ]
            char.setActionSeq(valid_acts)
            global config_updated
            config_updated = True
        else:
            print("No update")
    except Exception as e:
        print(e)
        traceback.print_exc()
        raise PreventUpdate

    return no_update


@app.callback(
    Output({"type": "char-actions-text", "index": MATCH}, "pattern"),
    Input({"type": "char-actions-text", "index": MATCH}, "value"),
    State({"type": "char-dropdown-config", "index": MATCH}, "value"),
)
def update_actions_css(actions, char_names):
    return "(basic)|(skill)"


# Populate Characters
for i in range(4):

    @app.callback(
        Output({"type": "char-dropdown-sim", "index": i}, "options"),
        Input("load-event", "n_intervals"),
    )
    def set_main_chars(_):
        return chars


for i in range(4):

    @app.callback(
        Output({"type": "char-dropdown-config", "index": i}, "options"),
        Input("load-event", "n_intervals"),
    )
    def set_config_chars(_):
        return chars


@app.callback(
    Output("char-dropdown-compare-view", "value"),
    Output("speed-sim-update", "data"),
    Input("nav-tabs", "active_tab"),
    Input("char-dropdown-compare", "value"),
    State("char-dropdown-compare-view", "value"),
    State("speed-sim-update", "data"),
)
def run_speed_simulation(current_tab, char, char_view, data_change):
    if current_tab == "tab-1":
        sim.run_speed_compare(char)

    if char_view is None or char_view == "None":
        return char, data_change + 1
    else:
        return no_update, data_change + 1


@app.callback(
    Output("speed-graph", "figure"),
    Input("speed-sim-update", "data"),
    Input("char-dropdown-compare-view", "value"),
    Input("nav-tabs", "active_tab"),
    State("char-dropdown-compare-view", "value"),
)
def update_speed_compare_graph(char_sim, char_view, tab, view_value):
    if tab == "tab-1":
        if (
            char_sim is None
            or char_sim == "None"
            or char_view is None
            or char_view == "None"
        ):
            logger.debug("Fields are empty, preventing update")
            raise PreventUpdate

        fig = go.Figure(
            layout=go.Layout(
                xaxis_title=f"Speed of {char_sim}",
                yaxis_title=f"Turns of {char_view}",
                legend_title=f"Turns for {char_view}",
            )
        )

        data = sim.speed_turn_data
        char_data = data[char_view]

        trace = go.Scatter(
            x=char_data["x_speed"],
            y=char_data["y_turns"],
            name=char_view,
        )
        fig.add_trace(trace)
        fig.update_yaxes({"range": (0, max(trace.y) + 1)})

        return fig
    else:
        raise PreventUpdate


@app.callback(
    Output("char-dropdown-compare", "options"),
    Output("char-dropdown-compare-view", "options"),
    Input("nav-tabs", "active_tab"),
)
def update_sim_compare_dropdown(tab):
    print("Tab change")
    if tab == "tab-1":
        return sim.character_names, sim.character_names
    else:
        return no_update
    
    
@app.callback(
    Output('turn-order-display', 'children'),
    Input('main-sim-update', 'data'),
    State('graph', 'figure')
)
def update_turn_order_display(_, fig):
    pprint(fig)
    # if show av in turn history
    r = []
    cycle_counter = 150
    for name, av in sim.turnHistory:
        if av > cycle_counter:
            r.append(
                dbc.ListGroupItem(f'{(cycle_counter / 75) - 1}', style={'color':'yellow'})
            )
            cycle_counter += 75
        r.append(
            dbc.ListGroupItem(f'{name} {av}', style={'color':colors[sim.character_names.index(name)]}),
        )
    return r

# Run the app
if __name__ == "__main__":
    app.run(
        host=("0.0.0.0" if os.environ.get("CONTAINER", False) else "localhost"),
        port=int(os.environ.get("PORT", 8050)),
        debug=True,
    )


# Configure page where you can set the character parameters, and action sequence, and targets
# Fix discrepency between base AV and avg AV
