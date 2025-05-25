import dash
from dash import html, dcc, Output, Input, State

from state import INITIAL_STATE, reduce, Action

app = dash.Dash(__name__)


class Database:
    def __init__(self):
        self._cities_by_county = {
            "France": ["Paris", "Lyon", "Marseille"],
            "USA": ["New York", "Los Angeles", "Chicago"],
            "Japan": ["Tokyo", "Kyoto", "Osaka"],
        }

    def get_countries(self) -> list[str]:
        return list(self._cities_by_county.keys())

    def get_cities(self, country: str) -> list[str]:
        return self._cities_by_county[country]


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

    state = reduce(state, Action.SELECT_COUNTRY, selected_country)
    state = reduce(
        state,
        Action.SETUP_CITY,
        {
            "options": db.get_cities(selected_country) if selected_country is not None else [],
            "value": None,
        },
    )
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

    return reduce(state, Action.SELECT_CITY, selected_city)


@app.callback(
    Output("state", "data", allow_duplicate=True),
    Input("message-input", "value"),
    State("state", "data"),
    prevent_initial_call=True,
)
def on_type_message(message: str, state: dict):
    if message == state["message-input"]["value"]:
        return dash.no_update

    return reduce(state, Action.SET_MESSAGE, message)


@app.callback(
    Output("state", "data"),
    Input("send-button", "n_clicks"),
    State("state", "data"),
    prevent_initial_call=True,
)
def on_click_send(n: int | None, state: dict):
    if n is None:
        return dash.no_update

    state = reduce(state, Action.SEND_MESSAGE)
    state = reduce(state, Action.SELECT_COUNTRY, None)
    state = reduce(state, Action.SETUP_CITY, {"options": [], "value": None})
    state = reduce(state, Action.SET_MESSAGE, "")
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
