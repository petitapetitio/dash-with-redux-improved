import dash
from dash import html, dcc, Output, Input, State

from database import Database
from state import (
    INITIAL_STATE,
    reduce,
    SetupCity,
    SelectCountry,
    SelectCity,
    SetMessage,
    SendMessage,
)

app = dash.Dash(__name__)

db = Database()

app.layout = html.Div(
    id="app-layout",
    children=[
        dcc.Store(id="state", data=INITIAL_STATE),
        html.Div(
            id="container",
            children=[
                html.H1("Send a message to"),
                html.Form(
                    [
                        dcc.Dropdown(
                            id="country-dropdown",
                            options=db.get_countries(),
                            value=INITIAL_STATE["country"],
                            placeholder="Select a country",
                            clearable=False,
                        ),
                        dcc.Dropdown(
                            id="city-dropdown",
                            placeholder="Select a city",
                            options=INITIAL_STATE["city-dropdown"]["options"],
                            value=INITIAL_STATE["city-dropdown"]["value"],
                            disabled=INITIAL_STATE["city-dropdown"]["disabled"],
                            clearable=False,
                        ),
                        dcc.Input(
                            id="message-input",
                            placeholder="Your message",
                            value=INITIAL_STATE["message-input"]["value"],
                            disabled=INITIAL_STATE["message-input"]["disabled"],
                        ),
                        html.Button(
                            id="send-button",
                            children="send",
                            disabled=INITIAL_STATE["send-button"]["disabled"],
                            type="button",
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
def on_select_country(selected_country: str | None, state: dict):
    if selected_country == state["country"]:
        return dash.no_update

    cities = db.get_cities(selected_country) if selected_country is not None else []

    state = reduce(state, SelectCountry(selected_country))
    state = reduce(state, SetupCity(options=cities, value=None))
    return state


@app.callback(
    Output("state", "data", allow_duplicate=True),
    Input("city-dropdown", "value"),
    State("state", "data"),
    prevent_initial_call=True,
)
def on_select_city(selected_city: str | None, state: dict):
    if selected_city == state["city-dropdown"]["value"]:
        return dash.no_update

    return reduce(state, SelectCity(selected_city))


@app.callback(
    Output("state", "data", allow_duplicate=True),
    Input("message-input", "value"),
    State("state", "data"),
    prevent_initial_call=True,
)
def on_type_message(message: str, state: dict):
    if message == state["message-input"]["value"]:
        return dash.no_update

    return reduce(state, SetMessage(message))


@app.callback(
    Output("state", "data"),
    Input("send-button", "n_clicks"),
    State("state", "data"),
    prevent_initial_call=True,
)
def on_click_send(n: int | None, state: dict):
    if n is None:
        return dash.no_update

    state = reduce(state, SendMessage())
    state = reduce(state, SelectCountry.reset())
    state = reduce(state, SetupCity.reset())
    state = reduce(state, SetMessage.reset())
    return state


@app.callback(
    Output("country-dropdown", "value"),
    Output("city-dropdown", "options"),
    Output("city-dropdown", "value"),
    Output("city-dropdown", "disabled"),
    Output("message-input", "value"),
    Output("message-input", "disabled"),
    Output("send-button", "value"),
    Output("send-button", "disabled"),
    Output("output", "children"),
    Input("state", "data"),
)
def on_update_state(state: dict):
    return (
        state["country"],
        state["city-dropdown"]["options"],
        state["city-dropdown"]["value"],
        state["city-dropdown"]["disabled"],
        state["message-input"]["value"],
        state["message-input"]["disabled"],
        None,
        state["send-button"]["disabled"],
        state["result"],
    )


if __name__ == "__main__":
    app.run()
