import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Output, Input, State

from state import INITIAL_STATE, CITIES_BY_COUNTRY, reduce, Action

app = dash.Dash(__name__)

app.layout = html.Div(
    id="app-layout",
    children=[
        dcc.Store(id="state", data=INITIAL_STATE),
        html.Div(
            id="container",
            children=[
                html.H1("Send a signal to"),
                html.Form(
                    [
                        html.Label("Country"),
                        dcc.Dropdown(
                            id="country-dropdown",
                            options=[
                                {"label": c, "value": c} for c in CITIES_BY_COUNTRY
                            ],
                            placeholder="Select a country",
                            clearable=False,
                        ),
                        html.Label("City"),
                        dcc.Dropdown(
                            id="city-dropdown",
                            placeholder="Select a city",
                            disabled=True,
                            clearable=False,
                        ),
                        html.Label("Signal"),
                        dcc.Dropdown(
                            id="signal-dropdown",
                            placeholder="Select a signal",
                            options=["PUSH", "HOLD"],
                            disabled=True,
                            clearable=False,
                        ),
                    ]
                ),
                html.Div(id="output"),
            ],
        ),
    ],
)


@app.callback(
    Output("state", "data", allow_duplicate=True),
    Input("country-dropdown", "value"),
    State("state", "data"),
    prevent_initial_call=True,
)
def on_select_country(selected_country, state: dict):
    return reduce(state, Action.SELECT_COUNTRY, selected_country)


@app.callback(
    Output("state", "data", allow_duplicate=True),
    Input("city-dropdown", "value"),
    State("state", "data"),
    prevent_initial_call=True,
)
def on_select_city(selected_city: str | None, state: dict):
    if selected_city is None:
        return dash.no_update

    return reduce(state, Action.SELECT_CITY, selected_city)


@app.callback(
    Output("state", "data"),
    Input("signal-dropdown", "value"),
    State("state", "data"),
    prevent_initial_call=True,
)
def on_click_submit_form(signal: str | None, state: dict):
    if signal is None:
        return dash.no_update

    return reduce(state, Action.SEND_SIGNAL, signal)


@app.callback(
    Output("city-dropdown", "options"),
    Output("city-dropdown", "value"),
    Output("city-dropdown", "disabled"),
    Output("signal-dropdown", "disabled"),
    Output("output", "children"),
    Input("state", "data"),
)
def on_update_state(state: dict):
    print("on_update_state")
    return (
        state["city-dropdown"]["options"],
        state["city-dropdown"]["value"],
        state["city-dropdown"]["disabled"],
        state["signal-dropdown"]["disabled"],
        state["result"],
    )


if __name__ == "__main__":
    app.run()
