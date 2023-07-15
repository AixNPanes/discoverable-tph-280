from typing import Optional
from .util import logger

from pahommqtt.client import Client, MQTTMessage
from ha_mqtt_discoverable import Settings
from discoverable_environmental_station_280.base import Units, GuageInfo, Guage


class HumidityUnits(Units):
    PERCENT = ("Percent", "%", lambda h: h)


class HygrometerInfo(GuageInfo):
    """Special information for Hygrometer"""

    component: str = "sensor"
    name: str = "My Hygrometer"
    object_id: Optional[str] = "my-hygrometer"
    device_class: Optional[str] = "humidity"
    units = HumidityUnits.PERCENT
    unique_id: Optional[str] = "my-hygrometer"


class Hygrometer(Guage):
    """Implements an MQTT hygrometer:
    https://www.home-assistant.io/integrations/sensor.mqtt/
    """

    value_name: str = "humidity"

    def __init__(
        cls,
        mqtt: Settings.MQTT,
        name: str = "Hygrometer",
        device_class="humidity",
    ):
        super(Hygrometer, cls).__init__(
            mqtt=mqtt,
            name=name,
            device_class=device_class,
            info_class=HygrometerInfo,
            callback=Hygrometer.command_callback,
        )

    def set_units(cls, unit: str):
        cls.units = HumidityUnits.units(unit)

    @staticmethod
    def command_callback(client: Client, user_data, message: MQTTMessage):
        callback_payload = message.payload.decode()
        logger.info(f"Hygrometer received {callback_payload} from HA")
