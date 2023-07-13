from __future__ import annotations
import logging
import logging.config
from typing import Any, Optional, TypeVar, Callable
import paho.mqtt.client as mqtt
from .util import logger

from ha_mqtt_discoverable import mqtt as MQTT
from discoverable_environmental_station_280.base import (
        Units,
        GuageInfo,
        Guage
        )

class TemperatureUnits(Units):
    CELSIUS = ("Celsius", "°C", lambda c: c)
    FARENHEIT = ("Farenheit", "°F", lambda c: 1.8 * c + 32)
    KELVIN = ("Kelvin", "°K", lambda c: c +273.15)

class ThermometerInfo(GuageInfo):
    """ Special information for Thermometer """
    component: str = "sensor"
    name: str = "My Thermometer"
    object_id: optional[str] = "my-thermometer"
    device_class: Optional[str] = "temperature"
    units = TemperatureUnits.CELSIUS
    unique_id: Otional[str] = "my-thermometer"

class Thermometer(Guage):
    """ Implements an MQTT thermometer:
    https://www.home-assistant.io/integrations/sensor.mqtt/
    """

    value_name:str = "temperature"

    def __init__(cls, mqtt:MQTT=None, name:str="Thermometer", \
            device_class='temperature'):
        super(Thermometer,cls).__init__(mqtt=mqtt, name=name, \
                device_class=device_class, info_class=ThermometerInfo,
                callback=Thermometer.command_callback)

    def set_units(cls, unit:str):
        cls.units = TemperatureUnits.units(unit)

    @staticmethod
    def command_callback(client: Client, user_data, message: MQQTMessage):
        callback_payload = message.payload.decode()
        logging.info(f'Thermometer received {callback_payload} from HA')