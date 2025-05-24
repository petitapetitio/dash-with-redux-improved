from enum import Enum, auto


INITIAL_STATE = {
    "country": None,
    "city-dropdown": {
        "options": [],
        "value": None,
        "disabled": True,
    },
    "signal-dropdown": {
        "disabled": True,
    },
    "result": ""
}

CITIES_BY_COUNTRY = {
    "France": ["Paris", "Lyon", "Marseille"],
    "USA": ["New York", "Los Angeles", "Chicago"],
    "Japan": ["Tokyo", "Kyoto", "Osaka"],
}


class Action(Enum):
    SELECT_COUNTRY = auto()
    SELECT_CITY = auto()
    SEND_SIGNAL = auto()


def reduce(state: dict, action: Action, payload=None) -> dict:
    if action == Action.SELECT_COUNTRY:
        cities = CITIES_BY_COUNTRY[payload]
        return state | {
            "country": payload,
            "city-dropdown": {
                "options": [{"label": city, "value": city} for city in cities],
                "value": None,
                "disabled": False,
            }
        }
    if action == Action.SELECT_CITY:
        return state | {
            "city-dropdown": {
                **state["city-dropdown"],
                "value": payload,
            },
            "signal-dropdown": {
                **state["signal-dropdown"],
                "disabled": False,
            },
        }
    if action == Action.SEND_SIGNAL:
        return state | {
            "result": f"You just sent {payload} to {state['city-dropdown']['value']} ({state['country']})."
        }

    raise NotImplementedError(f"Reducer for {action} isn't implemented.")
