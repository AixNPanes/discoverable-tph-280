from __future__ import annotations
import logging
import logging.config
from typing import Optional

from paho.mqtt.client import MQTTMessage
from ha_mqtt_discoverable import Client, mqtt as MQTT
from discoverable_tph_280.base import Units, GuageInfo, Guage


class PressureUnits(Units):
    HPA = ("HectoPascal", "hPa", lambda p: p)
    MBAR = ("MilliBar", "mbAR", lambda p: p)
    KPA = ("KiloPascal", "kPA", lambda p: 0.1 * p)
    CBAR = ("CentiBar", "cbar", lambda p: 0.1 * p)
    BAR = ("Bar", "bar", lambda p: 0.001 * p)
    INHG = ("inHg", "inHg", lambda p: 0.029529983071445 * p)
    MMHG = ("mmHg", "mmHg", lambda p: 0.75006157584566 * p)
    PA = ("Pascal", "Pa", lambda c: 100 * c)
    PSI = ("PoundsPerSquareInch", "PSI", lambda p: 0.0145 * p)


class BarometerInfo(GuageInfo):
    """Special information for Barometer"""

    component: str = "sensor"
    name: str = "My Barometer"
    object_id: Optional[str] = "my-barometer"
    device_class: Optional[str] = "pressure"
    units = PressureUnits.HPA
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

    def set_units(cls, unit: str):
        cls.units = PressureUnits.units(unit)

    @staticmethod
    def command_callback(client: Client, user_data, message: MQTTMessage):
        callback_payload = message.payload.decode()
        logging.info(f"Barometer received {callback_payload} from HA")
