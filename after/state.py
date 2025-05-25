from __future__ import annotations

from dataclasses import dataclass

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


class Action:
    pass


@dataclass(frozen=True)
class SelectCountry(Action):
    country: str | None

    @classmethod
    def reset(cls):
        return SelectCountry(None)


@dataclass(frozen=True)
class SetupCity(Action):
    options: tuple[str, ...]
    value: str | None

    @classmethod
    def reset(cls) -> SetupCity:
        return SetupCity(tuple(), None)


@dataclass(frozen=True)
class SelectCity(Action):
    city: str | None


@dataclass(frozen=True)
class SetMessage(Action):
    message: str

    @classmethod
    def reset(cls) -> SetMessage:
        return SetMessage("")


@dataclass(frozen=True)
class SendMessage(Action):
    pass


def reduce(state: dict, action: Action) -> dict:
    if isinstance(action, SelectCountry):
        return state | {
            "country": action.country,
        }

    if isinstance(action, SetupCity):
        return state | {
            "city-dropdown": {
                **state["city-dropdown"],
                "options": action.options,
                "value": action.value,
                "disabled": len(action.options) == 0,
            },
        }

    if isinstance(action, SelectCity):
        return state | {
            "city-dropdown": {
                **state["city-dropdown"],
                "value": action.city,
            },
            "message-input": {
                **state["message-input"],
                "disabled": False,
            },
        }

    if isinstance(action, SetMessage):
        return state | {
            "message-input": {
                **state["message-input"],
                "value": action.message,
            },
            "send-button": {
                "disabled": len(action.message) == 0,
            },
        }

    if isinstance(action, SendMessage):
        return state | {
            "result": f"You just sent « {state["message-input"]["value"]} » to {state['city-dropdown']['value']} ({state['country']}).",
            "message-input": {
                "value": "",
                "disabled": True,
            },
        }

    raise NotImplementedError(f"Reducer for {action} isn't implemented.")
