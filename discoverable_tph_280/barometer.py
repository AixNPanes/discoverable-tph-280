from __future__ import annotations
import logging
import logging.config
from typing import Optional

from paho.mqtt.client import MQTTMessage, mqtt as MQTT
from .base import GuageInfo, Guage


class BarometerInfo(GuageInfo):
    """Special information for Barometer"""

    component: str = "sensor"
    name: str = "My Barometer"
    object_id: Optional[str] = "my-barometer"
    device_class: Optional[str] = "pressure"
    unique_id: Optional[str] = "my-barometer"


class Barometer(Guage):
    """Implements an MQTT barometer:
    https://www.home-assistant.io/integrations/sensor.mqtt/
    """

    value_name: str = "pressure"

    def __init__(
        cls, mqtt: MQTT, name: str = "Barometer", device_class="pressure"
    ):
        super(Barometer, cls).__init__(
            mqtt=mqtt,
            name=name,
            device_class=device_class,
            info_class=BarometerInfo,
            callback=Barometer.command_callback,
        )

    @staticmethod
    def command_callback(client: MQTT, user_data, message: MQTTMessage):
        callback_payload = message.payload.decode()
        logging.info(f"Barometer received {callback_payload} from HA")
