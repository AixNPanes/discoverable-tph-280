from __future__ import annotations
from typing import Optional, Callable
from .util import logger

from ha_mqtt_discoverable import EntityInfo, Subscriber, Settings


class GuageInfo(EntityInfo):
    """Base class for other Info classes"""

    enabled_by_default: Optional[bool] = True

    retain: Optional[bool] = None
    """ If the published message should have the retain flag or not """

    value: float = 0
    native_unit_of_measure: str = None
    suggested_display_precision: int = 1


class Guage(Subscriber[GuageInfo]):
    def __init__(
        cls,
        mqtt: Settings.MQTT = None,
        name=None,
        device_class=None,
        info_class=None,
        callback=Callable,
    ):
        cls.info = info_class(name=name, device_class=device_class)
        cls.settings = Settings(mqtt=Settings.MQTT, entity=cls.info)
        super(Guage, cls).__init__(cls.settings, command_callback=callback)

    def set_value(cls, value):
        cls.value = value
        cls.set_attributes("value", cls.value)

    def get_value(cls) -> float:
        return cls.value

    def set_attributes(cls, name, value):
        logger.debug(f"sett_attributes {name}, {value}")
        cls._entity.value = value
        print(cls.value_name, cls._entity.value)
        super(Guage, cls).set_attributes(
            attributes={cls.value_name: cls._entity.value}
        )
        cls._send_action(state=cls.value)

    def _send_action(cls, state: str) -> None:
        logger.info(
            f"Sending {state} command to {cls._entity.name} \
                    using {cls.state_topic}"
        )
        cls._state_helper(state=state)
