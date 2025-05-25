from enum import Enum, auto


INITIAL_STATE = {
    "country": None,
    "city-dropdown": {
        "options": [],
        "value": None,
        "disabled": True,
    },
    "message-input": {
        "value": "",
        "disabled": True,
    },
    "send-button": {
        "disabled": True,
    },
    "result": "",
}


class Action(Enum):
    SELECT_COUNTRY = auto()
    SETUP_CITY = auto()
    SELECT_CITY = auto()
    SET_MESSAGE = auto()
    SEND_MESSAGE = auto()


def reduce(state: dict, action: Action, payload=None) -> dict:
    if action == Action.SELECT_COUNTRY:
        return state | {
            "country": payload,
        }
    if action == Action.SETUP_CITY:
        return state | {
            "city-dropdown": {
                "options": payload["options"],
                "value": payload["value"],
                "disabled": len(payload["options"]) == 0,
            },
        }

    if action == Action.SELECT_CITY:
        return state | {
            "city-dropdown": {
                **state["city-dropdown"],
                "value": payload,
            },
            "message-input": {
                **state["message-input"],
                "disabled": False,
            },
        }

    if action == Action.SET_MESSAGE:
        message = payload
        return state | {
            "message-input": {
                **state["message-input"],
                "value": message,
            },
            "send-button": {
                "disabled": len(message) == 0,
            },
        }
    if action == Action.SEND_MESSAGE:
        return state | {
            "result": f"You just sent « {state["message-input"]["value"]} » to {state['city-dropdown']['value']} ({state['country']}).",
            "message-input": {
                "value": "",
                "disabled": True,
            },
        }

    raise NotImplementedError(f"Reducer for {action} isn't implemented.")
