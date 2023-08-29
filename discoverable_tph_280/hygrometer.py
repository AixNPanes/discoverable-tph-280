from typing import Optional
from .util import logger

from paho.mqtt.client import MQTTMessage
from ha_mqtt_discoverable import Settings
from .base import GuageInfo, Guage


class HygrometerInfo(GuageInfo):
    """Special information for Hygrometer"""

    component: str = "sensor"
    name: str = "My Hygrometer"
    object_id: Optional[str] = "my-hygrometer"
    device_class: Optional[str] = "humidity"
    unique_id: Optional[str] = "my-hygrometer"


class Hygrometer(Guage):
    """Implements an MQTT hygrometer:
    https://www.home-assistant.io/integrations/sensor.mqtt/
    """

    value_name: str = "humidity"

    def __init__(
        cls,
        mqtt_settings: Settings.MQTT,
        name: str = "Hygrometer",
        device_class="humidity",
    ):
        super(Hygrometer, cls).__init__(
            mqtt_settings=mqtt_settings,
            name=name,
            device_class=device_class,
            info_class=HygrometerInfo,
            callback=Hygrometer.command_callback,
        )

    @staticmethod
    def command_callback(
        client: Settings.MQTT, user_data, message: MQTTMessage
    ):
        callback_payload = message.payload.decode()
        logger.info(f"Hygrometer received {callback_payload} from HA")
